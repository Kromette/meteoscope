from datetime import datetime
from unittest.mock import Mock

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from meteoscope.database.models import Location, WeatherObservation
from meteoscope.ingestion.models import (
    LocationData,
    WeatherObservationData,
)
from meteoscope.ingestion.service import WeatherIngestionService


def make_location() -> LocationData:
    return LocationData(
        latitude=48.8566,
        longitude=2.3522,
        timezone="Europe/Paris",
        elevation=35.0,
    )


def make_observation(timestamp: datetime) -> WeatherObservationData:
    return WeatherObservationData(
        timestamp=timestamp,
        temperature_2m=20.5,
        apparent_temperature=20.0,
        relative_humidity_2m=65,
        precipitation=0.0,
        precipitation_probability=10,
        weather_code=1,
        cloud_cover=30,
        wind_speed_10m=12.0,
        wind_direction_10m=180,
        wind_gusts_10m=20.0,
    )


def test_persist_weather_is_idempotent(test_session: Session) -> None:
    client = Mock()
    service = WeatherIngestionService(client=client)
    location = make_location()
    observations = [
        make_observation(datetime(2026, 9, 17, 10, 0)),
        make_observation(datetime(2026, 9, 17, 11, 0)),
    ]

    session = test_session
    session.execute(
        delete(WeatherObservation).where(
            WeatherObservation.location.has(
                latitude=location.latitude,
                longitude=location.longitude,
            )
        )
    )
    session.execute(
        delete(Location).where(
            Location.latitude == location.latitude,
            Location.longitude == location.longitude,
        )
    )
    session.commit()

    service.persist_weather(
        session,
        location=location,
        observations=observations,
    )
    session.commit()

    service.persist_weather(
        session,
        location=location,
        observations=observations,
    )
    session.commit()

    locations = session.execute(
        select(Location).where(
            Location.latitude == location.latitude,
            Location.longitude == location.longitude,
        )
    ).scalars().all()

    stored_observations = session.execute(
        select(WeatherObservation).where(
            WeatherObservation.location_id == locations[0].id
        )
    ).scalars().all()

    assert len(locations) == 1
    assert len(stored_observations) == 2
