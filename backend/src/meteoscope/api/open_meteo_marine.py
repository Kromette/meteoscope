import httpx

BASE_URL = "https://marine-api.open-meteo.com/v1/marine"

HOURLY_VARIABLES = (
    "wave_height",
    "wave_direction",
    "wave_period",
    "wave_peak_period",
    "sea_level_height_msl",
    "sea_surface_temperature",
    "ocean_current_velocity",
    "ocean_current_direction",
    "wind_wave_height",
    "wind_wave_direction",
    "wind_wave_period",
    "wind_wave_peak_period",
    "swell_wave_height",
    "swell_wave_direction",
    "swell_wave_period",
    "swell_wave_peak_period",
    "secondary_swell_wave_height",
    "secondary_swell_wave_period",
    "secondary_swell_wave_direction",
    "tertiary_swell_wave_height",
    "tertiary_swell_wave_period",
    "tertiary_swell_wave_direction",
)
CURRENT_VARIABLES = (
    "wave_height",
    "wave_direction",
    "wave_period",
    "wave_peak_period",
    "wind_wave_height",
    "wind_wave_direction",
    "wind_wave_period",
    "wind_wave_peak_period",
    "swell_wave_height",
    "swell_wave_direction",
    "swell_wave_period",
    "swell_wave_peak_period",
    "secondary_swell_wave_height",
    "secondary_swell_wave_period",
    "secondary_swell_wave_direction",
    "tertiary_swell_wave_height",
    "tertiary_swell_wave_period",
    "tertiary_swell_wave_direction",
    "sea_level_height_msl",
    "sea_surface_temperature",
    "ocean_current_velocity",
    "ocean_current_direction",
)
MINUTELY_15_VARIABLES = (
    "ocean_current_velocity",
    "ocean_current_direction",
    "sea_level_height_msl",
)


class OpenMeteoMarineClient:
    def __init__(
        self,
        client: httpx.Client | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._client = client or httpx.Client(timeout=timeout)

    def get_forecast(
        self,
        *,
        latitude: list[float],
        longitude: list[float],
    ) -> list[dict[str, str | float | int]]:

        if len(latitude) != len(longitude):
            raise ValueError("Latitude and longitude must have the same length.")

        params: dict[str, str | int | float | list[float]] = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(HOURLY_VARIABLES),
            "current": ",".join(CURRENT_VARIABLES),
            "forecast_days": 7,
            "timezone": "Europe/London",
            "timeformat": "unixtime",
            "minutely_15": ",".join(MINUTELY_15_VARIABLES),
            "past_minutely_15": 4,
            "forecast_minutely_15": 24,
        }

        response = self._client.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            raise ValueError("Open-Meteo Marine response must be a list.")

        return data
