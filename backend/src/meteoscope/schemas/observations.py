from datetime import date, datetime

from pydantic import BaseModel


class ObservationData(BaseModel):
    timestamp: datetime
    temperature_2m: float
    apparent_temperature: float
    relative_humidity_2m: float
    precipitation: float
    precipitation_probability: float
    weather_code: int
    cloud_cover: float
    wind_speed_10m: float
    wind_direction_10m: float
    wind_gusts_10m: float


class LocationData(BaseModel):
    latitude: float
    longitude: float


class ObservationsResponse(BaseModel):
    location: LocationData
    date: date
    timezone: str
    observations: list[ObservationData]
