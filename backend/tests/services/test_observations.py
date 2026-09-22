from datetime import date, datetime
from unittest.mock import Mock
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from meteoscope.api.open_meteo import OpenMeteoClient
from meteoscope.database.models import Location, WeatherObservation
from meteoscope.ingestion.service import WeatherIngestionService
from meteoscope.services.observations import ObservationsService


def test_returns_existing_complete_observations(test_session: Session) -> None:
    location = Location(
        latitude=48.8566,
        longitude=2.3522,
        timezone="Europe/Paris",
        elevation=35.0,
    )

    test_session.add(location)
    test_session.flush()

    location_timezone = ZoneInfo(location.timezone)

    observations = [
        WeatherObservation(
            location_id=location.id,
            timestamp=datetime(2026, 9, 17, hour, tzinfo=location_timezone),
            temperature_2m=15.0,
            apparent_temperature=14.5,
            relative_humidity_2m=70.0,
            precipitation=0.0,
            precipitation_probability=10.0,
            weather_code=1,
            cloud_cover=20.0,
            wind_speed_10m=10.0,
            wind_direction_10m=180.0,
            wind_gusts_10m=20.0,
        )
        for hour in range(24)
    ]

    test_session.add_all(observations)
    test_session.commit()

    ingestion_service = Mock(spec=WeatherIngestionService)

    service = ObservationsService(
        session=test_session,
        ingestion_service=ingestion_service,
    )

    response = service.get_observations(
        latitude=48.8566,
        longitude=2.3522,
        date=date(2026, 9, 17),
    )

    assert response.date == date(2026, 9, 17)
    assert response.timezone == "Europe/Paris"
    assert response.location.latitude == 48.8566
    assert response.location.longitude == 2.3522
    assert len(response.observations) == 24

    ingestion_service.fetch_weather.assert_not_called()


def test_fetches_weather_when_location_does_not_exist(test_session: Session) -> None:

    client = Mock(spec=OpenMeteoClient)

    client.get_forecast.return_value = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
        "elevation": 35.0,
        "hourly": {
            "time": [f"2026-09-17T{hour:02d}:00" for hour in range(24)],
            "temperature_2m": [15.0] * 24,
            "apparent_temperature": [14.5] * 24,
            "relative_humidity_2m": [70.0] * 24,
            "precipitation": [0.0] * 24,
            "precipitation_probability": [10.0] * 24,
            "weather_code": [1] * 24,
            "cloud_cover": [20.0] * 24,
            "wind_speed_10m": [10.0] * 24,
            "wind_direction_10m": [180.0] * 24,
            "wind_gusts_10m": [20.0] * 24,
        },
    }
    ingestion_service = WeatherIngestionService(client=client)

    service = ObservationsService(
        session=test_session,
        ingestion_service=ingestion_service,
    )

    response = service.get_observations(
        latitude=48.8566,
        longitude=2.3522,
        date=date(2026, 9, 17),
    )

    client.get_forecast.assert_called_once_with(
        latitude=48.8566,
        longitude=2.3522,
    )

    assert response.date == date(2026, 9, 17)
    assert response.timezone == "Europe/Paris"
    assert len(response.observations) == 24


def test_fetches_weather_when_observations_are_incomplete(
    test_session: Session,
) -> None:
    location = Location(
        latitude=48.8566,
        longitude=2.3522,
        timezone="Europe/Paris",
        elevation=35.0,
    )

    test_session.add(location)
    test_session.flush()

    location_timezone = ZoneInfo(location.timezone)

    observations = [
        WeatherObservation(
            location_id=location.id,
            timestamp=datetime(2026, 9, 17, hour, tzinfo=location_timezone),
            temperature_2m=15.0,
            apparent_temperature=14.5,
            relative_humidity_2m=70.0,
            precipitation=0.0,
            precipitation_probability=10.0,
            weather_code=1,
            cloud_cover=20.0,
            wind_speed_10m=10.0,
            wind_direction_10m=180.0,
            wind_gusts_10m=20.0,
        )
        for hour in range(23)  # Only 23 observations instead of 24
    ]

    test_session.add_all(observations)
    test_session.commit()

    client = Mock(spec=OpenMeteoClient)

    client.get_forecast.return_value = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
        "elevation": 35.0,
        "hourly": {
            "time": [f"2026-09-17T{hour:02d}:00" for hour in range(24)],
            "temperature_2m": [15.0] * 24,
            "apparent_temperature": [14.5] * 24,
            "relative_humidity_2m": [70.0] * 24,
            "precipitation": [0.0] * 24,
            "precipitation_probability": [10.0] * 24,
            "weather_code": [1] * 24,
            "cloud_cover": [20.0] * 24,
            "wind_speed_10m": [10.0] * 24,
            "wind_direction_10m": [180.0] * 24,
            "wind_gusts_10m": [20.0] * 24,
        },
    }

    ingestion_service = WeatherIngestionService(client=client)

    service = ObservationsService(
        session=test_session,
        ingestion_service=ingestion_service,
    )

    response = service.get_observations(
        latitude=48.8566,
        longitude=2.3522,
        date=date(2026, 9, 17),
    )

    client.get_forecast.assert_called_once_with(
        latitude=48.8566,
        longitude=2.3522,
    )

    assert response.date == date(2026, 9, 17)
    assert response.timezone == "Europe/Paris"
    assert len(response.observations) == 24
