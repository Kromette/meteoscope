from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from meteoscope.database.models import Location, WeatherObservation
from meteoscope.ingestion.service import WeatherIngestionService
from meteoscope.schemas.observations import (
    LocationData,
    ObservationData,
    ObservationsResponse,
)
from meteoscope.services.observation_datetime import is_complete_day


class ObservationsService:
    def __init__(
        self,
        session: Session,
        ingestion_service: WeatherIngestionService,
    ) -> None:
        self._session = session
        self._ingestion_service = ingestion_service

    def _build_date_range(
        self,
        *,
        date: date,
        timezone: str,
    ) -> tuple[datetime, datetime]:
        local_timezone = ZoneInfo(timezone)

        start_datetime = datetime.combine(
            date,
            time.min,
            tzinfo=local_timezone,
        )
        end_datetime = datetime.combine(
            date,
            time.max,
            tzinfo=local_timezone,
        ) + timedelta(microseconds=1)

        return start_datetime, end_datetime

    def _build_response(
        self,
        *,
        location: Location,
        date: date,
        observations: list[WeatherObservation],
    ) -> ObservationsResponse:
        return ObservationsResponse(
            location=LocationData(
                latitude=location.latitude,
                longitude=location.longitude,
            ),
            date=date,
            timezone=location.timezone,
            observations=[
                ObservationData(
                    timestamp=observation.timestamp,
                    temperature_2m=observation.temperature_2m,
                    apparent_temperature=observation.apparent_temperature,
                    relative_humidity_2m=observation.relative_humidity_2m,
                    precipitation=observation.precipitation,
                    precipitation_probability=observation.precipitation_probability,
                    weather_code=observation.weather_code,
                    cloud_cover=observation.cloud_cover,
                    wind_speed_10m=observation.wind_speed_10m,
                    wind_direction_10m=observation.wind_direction_10m,
                    wind_gusts_10m=observation.wind_gusts_10m,
                )
                for observation in observations
            ],
        )

    def _find_location(
        self,
        *,
        latitude: float,
        longitude: float,
    ) -> Location | None:
        return self._session.execute(
            select(Location).where(
                Location.latitude == latitude,
                Location.longitude == longitude,
            )
        ).scalar_one_or_none()

    def _find_observations(
        self,
        *,
        location_id: int,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[WeatherObservation]:
        return list(
            self._session.execute(
                select(WeatherObservation)
                .where(
                    WeatherObservation.location_id == location_id,
                    WeatherObservation.timestamp >= start_datetime,
                    WeatherObservation.timestamp < end_datetime,
                )
                .order_by(WeatherObservation.timestamp)
            )
            .scalars()
            .all()
        )

    def _fetch_and_persist_weather(
        self,
        *,
        latitude: float,
        longitude: float,
    ) -> None:
        location_data, observations_data = self._ingestion_service.fetch_weather(
            latitude=latitude,
            longitude=longitude,
        )

        self._ingestion_service.persist_weather(
            self._session,
            location=location_data,
            observations=observations_data,
        )

        self._session.commit()

    def get_observations(
        self,
        *,
        latitude: float,
        longitude: float,
        date: date,
    ) -> ObservationsResponse:

        location = self._find_location(latitude=latitude, longitude=longitude)

        if location is None:
            # case where location is not in the database,
            # we fetch and persist the weather data for that location
            self._fetch_and_persist_weather(
                latitude=latitude,
                longitude=longitude,
            )

            location = self._find_location(latitude=latitude, longitude=longitude)

            if location is None:
                raise RuntimeError("Location was not persisted correctly.")

        start_datetime, end_datetime = self._build_date_range(
            date=date, timezone=location.timezone
        )

        observations = self._find_observations(
            location_id=location.id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

        if not is_complete_day(observations, start_datetime, end_datetime):
            self._fetch_and_persist_weather(
                latitude=latitude,
                longitude=longitude,
            )
            observations = self._find_observations(
                location_id=location.id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
            )
            if not is_complete_day(observations, start_datetime, end_datetime):
                raise RuntimeError("Observations were not persisted correctly.")

        return self._build_response(
            location=location,
            date=date,
            observations=observations,
        )
