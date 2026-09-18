import httpx

BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

class GeocodingClient:
    def __init__(
        self,
        client: httpx.Client | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._client = client or httpx.Client(timeout=timeout)

    def search_locations(
        self,
        *,
        name: str,
        limit: int = 10,
        language: str = "fr",
    ) -> list[dict[str, object]]:
        params: dict[str, str | int] = {
            "name": name,
            "limit": limit,
            "language": language,
        }

        response = self._client.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            raise ValueError("Geocoding response must be a JSON array.")

        return data
