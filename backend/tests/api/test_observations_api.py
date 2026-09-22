from datetime import date
from unittest.mock import Mock

from fastapi.testclient import TestClient

from meteoscope.api.dependencies import get_observations_service
from meteoscope.main import app
from meteoscope.services.observations import ObservationsService

client = TestClient(app)

def test_get_observations_valid_request() -> None:
    service = Mock(spec=ObservationsService)

    expected_response = {
        "location": {
            "latitude": 48.8566,
            "longitude": 2.3522,
        },
        "date": "2026-09-17",
        "timezone": "Europe/Paris",
        "observations": [
            {
                "timestamp": f"2026-09-17T{hour:02d}:00:00+02:00",
                "temperature_2m": 15.0,
                "apparent_temperature": 14.5,
                "relative_humidity_2m": 70.0,
                "precipitation": 0.0,
                "precipitation_probability": 10.0,
                "weather_code": 1,
                "cloud_cover": 20.0,
                "wind_speed_10m": 10.0,
                "wind_direction_10m": 180.0,
                "wind_gusts_10m": 20.0,
            }
            for hour in range(24)
        ],
    }

    service.get_observations.return_value = expected_response

    app.dependency_overrides[get_observations_service] = lambda: service

    response = client.get(
        "/observations",
        params={
            "latitude": 48.8566,
            "longitude": 2.3522,
            "date": "2026-09-17",
        },
    )

    assert response.status_code == 200
    assert response.json() == expected_response

    service.get_observations.assert_called_once_with(
        latitude=48.8566,
        longitude=2.3522,
        date=date(2026, 9, 17),
    )

    app.dependency_overrides.clear()


def test_get_observations_rejects_invalid_latitude() -> None:
    response = client.get(
        "/observations",
        params={
            "latitude": "invalid_latitude",
            "longitude": 2.3522,
            "date": "2026-09-17",
        },
    )

    assert response.status_code == 422


def test_get_observations_requires_parameters() -> None:
    response = client.get(
        "/observations",
        params={
            "longitude": 2.3522,
            "date": "2026-09-17",
        },
    )

    assert response.status_code == 422