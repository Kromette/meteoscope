from typing import Annotated

from fastapi import APIRouter, Depends, Query

from meteoscope.api.dependencies import get_location_search_service
from meteoscope.schemas.locations import LocationSearchResponse
from meteoscope.services.location_search import LocationSearchService

router = APIRouter()


@router.get("/locations/search")
def search_locations(
    service: Annotated[
        LocationSearchService,
        Depends(get_location_search_service),
    ],
    name: str = Query(min_length=1),
    limit: int = Query(default=10, ge=1, le=10),
) -> LocationSearchResponse:
    return service.search_locations(
        name=name,
        limit=limit,
        language="fr",
    )
