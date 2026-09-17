import httpx

from meteoscope.api.open_meteo import (
    HOURLY_VARIABLES,
    OpenMeteoClient,
)


def test_get_forecast_returns_response() -> None:
    expected_response = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
        "hourly": {
            "time": ["2026-09-16T15:00"],
            "temperature_2m": [20.5],
        },
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/forecast"
        assert request.url.params["latitude"] == "48.8566"
        assert request.url.params["longitude"] == "2.3522"
        assert request.url.params["timezone"] == "Europe/Paris"
        assert request.url.params["hourly"] == ",".join(HOURLY_VARIABLES)
        assert request.url.params["past_days"] == "7"
        assert request.url.params["forecast_days"] == "0"

        return httpx.Response(200, json=expected_response)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = OpenMeteoClient(client=http_client)

    response = client.get_forecast(
        latitude=48.8566,
        longitude=2.3522,
        timezone="Europe/Paris",
    )

    assert response == expected_response


def test_get_forecast_raises_for_http_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = OpenMeteoClient(client=http_client)

    try:
        client.get_forecast(
            latitude=48.8566,
            longitude=2.3522,
            timezone="Europe/Paris",
        )
    except httpx.HTTPStatusError as exc:
        assert exc.response.status_code == 500
    else:
        raise AssertionError("Expected httpx.HTTPStatusError")
