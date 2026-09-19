from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends

from meteoscope.api.dependencies import get_observations_service
from meteoscope.schemas.observations import ObservationsResponse
from meteoscope.services.observations import ObservationsService

router = APIRouter()


@router.get("/observations")
def get_observations(
    service: Annotated[
        ObservationsService,
        Depends(get_observations_service),
    ],
    latitude: float,
    longitude: float,
    date: date,
) -> ObservationsResponse:
    return service.get_observations(latitude=latitude, longitude=longitude, date=date)
