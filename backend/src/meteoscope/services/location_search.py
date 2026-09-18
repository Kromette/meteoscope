
from meteoscope.api.geocoding import GeocodingClient


class LocationSearchService:
    def __init__(self, client: GeocodingClient) -> None:
        self._client = client

    def search_locations(
        self,
        *,
        name: str,
        limit: int = 10,
        language: str = "fr",
    ) -> list[dict[str, object]]:
        return self._client.search_locations(name=name, limit=limit, language=language)