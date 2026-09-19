from meteoscope.api.open_meteo import OpenMeteoClient
from meteoscope.config import (
    METEOSCOPE_LATITUDE,
    METEOSCOPE_LONGITUDE,
    METEOSCOPE_TIMEZONE,
)
from meteoscope.database.connection import SessionLocal
from meteoscope.ingestion.service import WeatherIngestionService


def main() -> None:
    client = OpenMeteoClient()
    service = WeatherIngestionService(client=client)

    with SessionLocal() as session:
        location, observations = service.fetch_weather(
            latitude=METEOSCOPE_LATITUDE,
            longitude=METEOSCOPE_LONGITUDE,
            timezone=METEOSCOPE_TIMEZONE,
        )

        service.persist_weather(
            session,
            location=location,
            observations=observations,
        )

        session.commit()


if __name__ == "__main__":
    main()
