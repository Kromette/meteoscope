from meteoscope.api.open_meteo import OpenMeteoClient
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