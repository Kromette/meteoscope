from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from meteoscope.api.geocoding import GeocodingClient
from meteoscope.api.open_meteo import OpenMeteoClient
from meteoscope.database.connection import get_db_session
from meteoscope.ingestion.service import WeatherIngestionService
from meteoscope.services.location_search import LocationSearchService
from meteoscope.services.observations import ObservationsService


def get_location_search_service() -> LocationSearchService:
    client = GeocodingClient()
    return LocationSearchService(client=client)


def get_observations_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> ObservationsService:
    client = OpenMeteoClient()

    return ObservationsService(
        session=session,
        ingestion_service=WeatherIngestionService(client=client),
    )
