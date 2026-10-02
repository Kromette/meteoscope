from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from meteoscope.api.open_meteo_marine import OpenMeteoMarineClient
from meteoscope.schemas.marine import (
    LocationData,
    MarineCurrentData,
    MarineHourlyData,
    MarineLocationData,
    MarineMinutelyData,
    MarineResponse,
)


class MarineService:
    def __init__(
        self,
        client: OpenMeteoMarineClient,
    ) -> None:
        self._client = client

    def _parse_location(
        self,
        data: dict[str, Any],
    ) -> MarineLocationData:
        current = data["current"]
        minutely_15 = data["minutely_15"]
        hourly = data["hourly"]

        location_timezone = ZoneInfo(data["timezone"])

        return MarineLocationData(
            location=LocationData(
                latitude=data["latitude"],
                longitude=data["longitude"],
            ),
            date=datetime.fromtimestamp(
                current["time"],
                tz=location_timezone,
            ).date(),
            timezone=data["timezone"],
            marine_current=self._parse_current(
                current,
                location_timezone,
            ),
            marine_minutely_15=self._parse_minutely_15(
                minutely_15,
                location_timezone,
            ),
            marine_hourly=self._parse_hourly(
                hourly,
                location_timezone,
            ),
        )

    def _parse_current(
        self,
        data: dict[str, Any],
        location_timezone: ZoneInfo,
    ) -> MarineCurrentData:
        return MarineCurrentData(
            timestamp=datetime.fromtimestamp(
                data["time"],
                tz=location_timezone,
            ),
            wave_height=data["wave_height"],
            wave_direction=data["wave_direction"],
            wave_period=data["wave_period"],
            wave_peak_period=data["wave_peak_period"],
            wind_wave_height=data["wind_wave_height"],
            wind_wave_direction=data["wind_wave_direction"],
            wind_wave_period=data["wind_wave_period"],
            wind_wave_peak_period=data["wind_wave_peak_period"],
            swell_wave_height=data["swell_wave_height"],
            swell_wave_direction=data["swell_wave_direction"],
            swell_wave_period=data["swell_wave_period"],
            swell_wave_peak_period=data["swell_wave_peak_period"],
            secondary_swell_wave_height=data["secondary_swell_wave_height"],
            secondary_swell_wave_period=data["secondary_swell_wave_period"],
            secondary_swell_wave_direction=data["secondary_swell_wave_direction"],
            tertiary_swell_wave_height=data["tertiary_swell_wave_height"],
            tertiary_swell_wave_period=data["tertiary_swell_wave_period"],
            tertiary_swell_wave_direction=data["tertiary_swell_wave_direction"],
            sea_level_height_msl=data["sea_level_height_msl"],
            sea_surface_temperature=data["sea_surface_temperature"],
            ocean_current_velocity=data["ocean_current_velocity"],
            ocean_current_direction=data["ocean_current_direction"],
        )

    def _parse_minutely_15(
        self,
        data: dict[str, Any],
        location_timezone: ZoneInfo,
    ) -> list[MarineMinutelyData]:
        return [
            MarineMinutelyData(
                timestamp=datetime.fromtimestamp(
                    timestamp,
                    tz=location_timezone,
                ),
                ocean_current_velocity=data["ocean_current_velocity"][index],
                ocean_current_direction=data["ocean_current_direction"][index],
                sea_level_height_msl=data["sea_level_height_msl"][index],
            )
            for index, timestamp in enumerate(data["time"])
        ]

    def _parse_hourly(
        self,
        data: dict[str, Any],
        location_timezone: ZoneInfo,
    ) -> list[MarineHourlyData]:
        return [
            MarineHourlyData(
                timestamp=datetime.fromtimestamp(
                    timestamp,
                    tz=location_timezone,
                ),
                wave_height=data["wave_height"][index],
                wave_direction=data["wave_direction"][index],
                wave_period=data["wave_period"][index],
                wave_peak_period=data["wave_peak_period"][index],
                wind_wave_height=data["wind_wave_height"][index],
                wind_wave_direction=data["wind_wave_direction"][index],
                wind_wave_period=data["wind_wave_period"][index],
                wind_wave_peak_period=data["wind_wave_peak_period"][index],
                swell_wave_height=data["swell_wave_height"][index],
                swell_wave_direction=data["swell_wave_direction"][index],
                swell_wave_period=data["swell_wave_period"][index],
                swell_wave_peak_period=data["swell_wave_peak_period"][index],
                secondary_swell_wave_height=data["secondary_swell_wave_height"][index],
                secondary_swell_wave_period=data["secondary_swell_wave_period"][index],
                secondary_swell_wave_direction=data["secondary_swell_wave_direction"][
                    index
                ],
                tertiary_swell_wave_height=data["tertiary_swell_wave_height"][index],
                tertiary_swell_wave_period=data["tertiary_swell_wave_period"][index],
                tertiary_swell_wave_direction=data["tertiary_swell_wave_direction"][
                    index
                ],
                sea_level_height_msl=data["sea_level_height_msl"][index],
                sea_surface_temperature=data["sea_surface_temperature"][index],
                ocean_current_velocity=data["ocean_current_velocity"][index],
                ocean_current_direction=data["ocean_current_direction"][index],
            )
            for index, timestamp in enumerate(data["time"])
        ]

    @staticmethod
    def _build_timestamps(
        *,
        start: int,
        end: int,
        interval: int,
        location_timezone: ZoneInfo,
    ) -> list[datetime]:
        return [
            datetime.fromtimestamp(
                timestamp,
                tz=location_timezone,
            )
            for timestamp in range(start, end, interval)
        ]

    def get_marine_data(
        self,
        *,
        latitude: list[float],
        longitude: list[float],
    ) -> MarineResponse:
        data = self._client.get_forecast(
            latitude=latitude,
            longitude=longitude,
        )

        locations = [self._parse_location(location_data) for location_data in data]

        return MarineResponse(locations=locations)
