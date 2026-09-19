from meteoscope.api.geocoding import GeocodingClient
from meteoscope.schemas.locations import LocationSearchResponse, LocationSearchResult


class LocationSearchService:
    def __init__(self, client: GeocodingClient) -> None:
        self._client = client

    def search_locations(
        self,
        *,
        name: str,
        limit: int = 10,
        language: str = "fr",
    ) -> LocationSearchResponse:

        response = self._client.search_locations(
            name=name,
            limit=limit,
            language=language,
        )

        results = response.get("results", [])

        if not isinstance(results, list):
            raise ValueError("Geocoding results must be a list.")

        return LocationSearchResponse(
            results=[
                LocationSearchResult(
                    name=result["name"],
                    latitude=result["latitude"],
                    longitude=result["longitude"],
                    country=result["country"],
                    country_code=result["country_code"],
                    admin1=result.get("admin1"),
                    timezone=result["timezone"],
                )
                for result in results
            ]
        )
