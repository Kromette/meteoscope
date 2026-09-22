from unittest.mock import Mock

from fastapi.testclient import TestClient

from meteoscope.api.dependencies import get_location_search_service
from meteoscope.main import app
from meteoscope.services.location_search import LocationSearchService

client = TestClient(app)


def test_search_locations() -> None:
    expected_response = {
        "results": [
            {
                "name": "Paris",
                "latitude": 48.85341,
                "longitude": 2.3488,
                "country": "France",
                "country_code": "FR",
                "admin1": "Île-de-France",
                "timezone": "Europe/Paris",
            }
        ]
    }

    service = Mock(spec=LocationSearchService)
    service.search_locations.return_value = expected_response

    app.dependency_overrides[get_location_search_service] = lambda: service

    response = client.get(
        "/locations/search",
        params={
            "name": "Paris",
            "limit": 10,
        },
    )

    assert response.status_code == 200
    assert response.json() == expected_response

    service.search_locations.assert_called_once_with(
        name="Paris",
        limit=10,
        language="fr",
    )

    app.dependency_overrides.clear()
