from datetime import datetime
from unittest.mock import Mock
from zoneinfo import ZoneInfo

from meteoscope.ingestion.models import (
    LocationData,
    WeatherObservationData,
)
from meteoscope.ingestion.service import WeatherIngestionService


def test_fetch_weather_fetches_and_parses_forecast() -> None:
    response = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
        "elevation": 35.0,
        "hourly": {
            "time": ["2026-09-17T10:00"],
            "temperature_2m": [20.5],
            "apparent_temperature": [20.0],
            "relative_humidity_2m": [65],
            "precipitation": [0.0],
            "precipitation_probability": [10],
            "weather_code": [1],
            "cloud_cover": [30],
            "wind_speed_10m": [12.0],
            "wind_direction_10m": [180],
            "wind_gusts_10m": [20.0],
        },
    }

    client = Mock()
    client.get_forecast.return_value = response

    service = WeatherIngestionService(client=client)

    location, observations = service.fetch_weather(
        latitude=48.8566,
        longitude=2.3522,
        timezone="Europe/Paris",
    )

    assert location == LocationData(
        latitude=48.8566,
        longitude=2.3522,
        timezone="Europe/Paris",
        elevation=35.0,
    )

    assert observations == [
        WeatherObservationData(
            timestamp=datetime(2026, 9, 17, 10, 0, tzinfo=ZoneInfo("Europe/Paris")),
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
    ]

    client.get_forecast.assert_called_once_with(
        latitude=48.8566,
        longitude=2.3522,
        timezone="Europe/Paris",
    )
