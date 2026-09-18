from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class LocationData:
    latitude: float
    longitude: float
    timezone: str
    elevation: float


@dataclass(frozen=True)
class WeatherObservationData:
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
