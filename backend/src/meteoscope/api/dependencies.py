from meteoscope.api.geocoding import GeocodingClient
from meteoscope.services.location_search import LocationSearchService


def get_location_search_service() -> LocationSearchService:
    client = GeocodingClient()
    return LocationSearchService(client=client)
