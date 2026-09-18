from pydantic import BaseModel


class LocationSearchResult(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: str
    country_code: str
    admin1: str | None = None
    timezone: str


class LocationSearchResponse(BaseModel):
    results: list[LocationSearchResult]