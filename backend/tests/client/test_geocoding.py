import httpx

from meteoscope.api.geocoding import GeocodingClient


def test_search_locations_returns_response() -> None:
    expected_response = [{
        "results": [
            {
                "id": 2988507,
                "name": "Paris",
                "latitude": 48.85341,
                "longitude": 2.3488,
                "elevation": 42.0,
                "feature_code": "PPLC",
                "country_code": "FR",
                "timezone": "Europe/Paris",
                "population": 2138551,
                "country": "France",
                "admin1": "Île-de-France",
                "admin2": "Département de Paris",
                "admin3": "Paris",
                "admin4": "Paris",
            }
        ],
    }]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/search"
        assert request.url.params["name"] == "Paris"
        assert request.url.params["limit"] == "10"
        assert request.url.params["language"] == "fr"

        return httpx.Response(200, json=expected_response)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = GeocodingClient(client=http_client)

    response = client.search_locations(
        name="Paris",
        limit=10,
    )

    assert response == expected_response