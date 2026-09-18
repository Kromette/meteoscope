from fastapi import APIRouter

from meteoscope.api.geocoding import GeocodingClient
from meteoscope.services.location_search import LocationSearchService

router = APIRouter()

@router.get("/locations/search")
def search_locations(
    name: str, 
    limit: int = 10, 
    language: str = "fr") -> object:

    client = GeocodingClient()
    service = LocationSearchService(client=client)
    result = service.search_locations(name=name, limit=limit, language=language)
    return {"status": "ok", "result": result}