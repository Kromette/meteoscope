from typing import Any

import httpx

BASE_URL = "https://api.open-meteo.com/v1/forecast"

HOURLY_VARIABLES = (
    "temperature_2m",
    "apparent_temperature",
    "relative_humidity_2m",
    "precipitation",
    "precipitation_probability",
    "weather_code",
    "cloud_cover",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
)


class OpenMeteoClient:
    def __init__(
        self,
        client: httpx.Client | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._client = client or httpx.Client(timeout=timeout)

    def get_forecast(
        self,
        *,
        latitude: float,
        longitude: float,
        timezone: str,
    ) -> dict[str, Any]:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(HOURLY_VARIABLES),
            "timezone": timezone,
        }

        response = self._client.get(BASE_URL, params=params)
        response.raise_for_status()

        return response.json()
