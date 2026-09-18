from unittest.mock import Mock

from meteoscope.api.geocoding import GeocodingClient
from meteoscope.services.location_search import LocationSearchService


def test_search_locations_returns_client_response() -> None:
    expected_response = [{
        "results": [
            {
                "id": 2988507,
                "name": "Paris",
                "latitude": 48.85341,
                "longitude": 2.3488,
                "country": "France",
                "country_code": "FR",
            }
        ]
    }]

    geocoding_client = Mock(spec=GeocodingClient)
    geocoding_client.search_locations.return_value = expected_response

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