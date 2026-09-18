from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from meteoscope.ingestion.models import (
    LocationData,
    WeatherObservationData,
)

HOURLY_FIELDS = (
    "temperature_2m",
    "apparent_temperature",
    "relative_humidity_2m",
    "precipitation",
    "precipitation_probability",
    "weather_code",
    "cloud_cover",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
)


def parse_forecast(
    data: dict[str, Any],
) -> tuple[LocationData, list[WeatherObservationData]]:
    location = _parse_location(data)
    observations = _parse_observations(data)

    return location, observations


def _parse_location(data: dict[str, Any]) -> LocationData:
    return LocationData(
        latitude=data["latitude"],
        longitude=data["longitude"],
        timezone=ZoneInfo(data["timezone"]),
        elevation=data["elevation"],
    )


def _parse_observations(
    data: dict[str, Any],
) -> list[WeatherObservationData]:
    hourly = data["hourly"]

    times = hourly["time"]
    values = {field: hourly[field] for field in HOURLY_FIELDS}

    lengths = {len(series) for series in values.values()}
    lengths.add(len(times))

    if len(lengths) != 1:
        raise ValueError("Hourly data arrays must have the same length.")

    observations = []
    local_timezone = ZoneInfo(data["timezone"])

    for index, timestamp in enumerate(times):
        observations.append(
            WeatherObservationData(
                timestamp = datetime.fromisoformat(timestamp)
                    .replace(tzinfo=local_timezone),
                temperature_2m=values["temperature_2m"][index],
                apparent_temperature=values["apparent_temperature"][index],
                relative_humidity_2m=values["relative_humidity_2m"][index],
                precipitation=values["precipitation"][index],
                precipitation_probability=values[
                    "precipitation_probability"
                ][index],
                weather_code=values["weather_code"][index],
                cloud_cover=values["cloud_cover"][index],
                wind_speed_10m=values["wind_speed_10m"][index],
                wind_direction_10m=values["wind_direction_10m"][index],
                wind_gusts_10m=values["wind_gusts_10m"][index],
            )
        )

    return observations
