# ruff: noqa: B008
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from meteoscope.api.dependencies import get_marine_service
from meteoscope.schemas.marine import MarineResponse
from meteoscope.services.marine import MarineService

router = APIRouter()


@router.get("/marine")
def get_marine_weather(
    service: Annotated[
        MarineService,
        Depends(get_marine_service),
    ],
    latitude: list[float] = Query(..., ge=-90, le=90),
    longitude: list[float] = Query(..., ge=-180, le=180),
) -> MarineResponse:
    return service.get_marine_data(latitude=latitude, longitude=longitude)
