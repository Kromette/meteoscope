from datetime import date, datetime

from pydantic import BaseModel


class MarineHourlyData(BaseModel):
    timestamp: datetime

    wave_height: float
    wave_direction: float
    wave_period: float
    wave_peak_period: float | None

    wind_wave_height: float
    wind_wave_direction: float
    wind_wave_period: float
    wind_wave_peak_period: float | None

    swell_wave_height: float
    swell_wave_direction: float
    swell_wave_period: float
    swell_wave_peak_period: float | None

    secondary_swell_wave_height: float
    secondary_swell_wave_period: float
    secondary_swell_wave_direction: float

    tertiary_swell_wave_height: float | None
    tertiary_swell_wave_period: float | None
    tertiary_swell_wave_direction: float | None

    sea_level_height_msl: float
    sea_surface_temperature: float
    ocean_current_velocity: float
    ocean_current_direction: float


class MarineCurrentData(BaseModel):
    timestamp: datetime

    wave_height: float
    wave_direction: float
    wave_period: float
    wave_peak_period: float | None

    wind_wave_height: float
    wind_wave_direction: float
    wind_wave_period: float
    wind_wave_peak_period: float | None

    swell_wave_height: float
    swell_wave_direction: float
    swell_wave_period: float
    swell_wave_peak_period: float | None

    secondary_swell_wave_height: float
    secondary_swell_wave_period: float
    secondary_swell_wave_direction: float

    tertiary_swell_wave_height: float | None
    tertiary_swell_wave_period: float | None
    tertiary_swell_wave_direction: float | None

    sea_level_height_msl: float
    sea_surface_temperature: float
    ocean_current_velocity: float
    ocean_current_direction: float


class MarineMinutelyData(BaseModel):
    timestamp: datetime
    ocean_current_velocity: float
    ocean_current_direction: float
    sea_level_height_msl: float


class LocationData(BaseModel):
    latitude: float
    longitude: float


class MarineLocationData(BaseModel):
    location: LocationData
    date: date
    timezone: str
    marine_current: MarineCurrentData
    marine_minutely_15: list[MarineMinutelyData]
    marine_hourly: list[MarineHourlyData]


class MarineResponse(BaseModel):
    locations: list[MarineLocationData]
