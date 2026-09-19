from unittest.mock import Mock

from meteoscope.api.geocoding import GeocodingClient
from meteoscope.schemas.locations import (
    LocationSearchResponse,
    LocationSearchResult,
)
from meteoscope.services.location_search import LocationSearchService


def test_search_locations_returns_response() -> None:
    client_response = {
        "results": [
            {
                "id": 2988507,
                "name": "Paris",
                "latitude": 48.85341,
                "longitude": 2.3488,
                "country": "France",
                "country_code": "FR",
                "timezone": "Europe/Paris",
            }
        ]
    }

    expected_response = LocationSearchResponse(
        results=[
            LocationSearchResult(
                name="Paris",
                latitude=48.85341,
                longitude=2.3488,
                country="France",
                country_code="FR",
                timezone="Europe/Paris",
            )
        ]
    )

    geocoding_client = Mock(spec=GeocodingClient)
    geocoding_client.search_locations.return_value = client_response

    service = LocationSearchService(geocoding_client)

    response = service.search_locations(
        name="Paris",
        limit=10,
        language="fr",
    )

    geocoding_client.search_locations.assert_called_once_with(
        name="Paris",
        limit=10,
        language="fr",
    )

    assert response == expected_response
