from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from meteoscope.api.open_meteo import OpenMeteoClient
from meteoscope.database.models import Location, WeatherObservation
from meteoscope.ingestion.models import (
    LocationData,
    WeatherObservationData,
)
from meteoscope.ingestion.parser import parse_forecast


class WeatherIngestionService:
    def __init__(self, client: OpenMeteoClient) -> None:
        self._client = client

    def fetch_weather(
        self,
        *,
        latitude: float,
        longitude: float,
        timezone: str,
    ) -> tuple[LocationData, list[WeatherObservationData]]:
        response = self._client.get_forecast(
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
        )

        return parse_forecast(response)

    def persist_weather(
        self,
        session: Session,
        *,
        location: LocationData,
        observations: list[WeatherObservationData],
    ) -> None:
        location_insert = insert(Location).values(
            latitude=location.latitude,
            longitude=location.longitude,
            timezone=location.timezone,
            elevation=location.elevation,
        )

        location_insert = location_insert.on_conflict_do_nothing(
            constraint="uq_locations_coordinates",
        )

        session.execute(location_insert)

        location_id = session.execute(
            select(Location.id).where(
                Location.latitude == location.latitude,
                Location.longitude == location.longitude,
            )
        ).scalar_one()

        observation_values = [
            {
                "location_id": location_id,
                "timestamp": observation.timestamp,
                "temperature_2m": observation.temperature_2m,
                "apparent_temperature": observation.apparent_temperature,
                "relative_humidity_2m": observation.relative_humidity_2m,
                "precipitation": observation.precipitation,
                "precipitation_probability": (observation.precipitation_probability),
                "weather_code": observation.weather_code,
                "cloud_cover": observation.cloud_cover,
                "wind_speed_10m": observation.wind_speed_10m,
                "wind_direction_10m": observation.wind_direction_10m,
                "wind_gusts_10m": observation.wind_gusts_10m,
            }
            for observation in observations
        ]

        if not observation_values:
            return

        observation_insert = insert(WeatherObservation).values(observation_values)

        observation_insert = observation_insert.on_conflict_do_nothing(
            index_elements=[
                WeatherObservation.location_id,
                WeatherObservation.timestamp,
            ],
        )

        session.execute(observation_insert)
