from datetime import datetime
from typing import Any

import pytest

from meteoscope.ingestion.models import (
    LocationData,
    WeatherObservationData,
)
from meteoscope.ingestion.parser import parse_forecast


def make_forecast_response() -> dict[str, Any]:
    return {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
        "elevation": 35.0,
        "hourly": {
            "time": [
                "2026-09-16T15:00",
                "2026-09-16T16:00",
            ],
            "temperature_2m": [20.5, 21.0],
            "apparent_temperature": [20.0, 20.7],
            "relative_humidity_2m": [65, 60],
            "precipitation": [0.0, 0.2],
            "precipitation_probability": [10, 20],
            "weather_code": [1, 2],
            "cloud_cover": [30, 40],
            "wind_speed_10m": [12.0, 14.0],
            "wind_direction_10m": [180, 190],
            "wind_gusts_10m": [20.0, 22.0],
        },
    }


def test_parse_forecast_returns_location_and_observations() -> None:
    data = make_forecast_response()

    location, observations = parse_forecast(data)

    assert location == LocationData(
        latitude=48.8566,
        longitude=2.3522,
        timezone="Europe/Paris",
        elevation=35.0,
    )

    assert observations == [
        WeatherObservationData(
            timestamp=datetime(2026, 9, 16, 15, 0),
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
        ),
        WeatherObservationData(
            timestamp=datetime(2026, 9, 16, 16, 0),
            temperature_2m=21.0,
            apparent_temperature=20.7,
            relative_humidity_2m=60,
            precipitation=0.2,
            precipitation_probability=20,
            weather_code=2,
            cloud_cover=40,
            wind_speed_10m=14.0,
            wind_direction_10m=190,
            wind_gusts_10m=22.0,
        ),
    ]


def test_parse_forecast_rejects_mismatched_hourly_lengths() -> None:
    data = make_forecast_response()
    data["hourly"]["temperature_2m"] = [20.5]

    with pytest.raises(ValueError, match="same length"):
        parse_forecast(data)
