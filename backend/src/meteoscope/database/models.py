from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime, Float


class Base(DeclarativeBase):
    pass


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    timezone: Mapped[str] = mapped_column(Text, nullable=False)
    elevation: Mapped[float] = mapped_column(Float, nullable=False)

    observations: Mapped[list["WeatherObservation"]] = relationship(
        back_populates="location",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint("latitude BETWEEN -90 AND 90", name="ck_locations_latitude"),
        CheckConstraint(
            "longitude BETWEEN -180 AND 180",
            name="ck_locations_longitude",
        ),
        UniqueConstraint(
            "latitude",
            "longitude",
            name="uq_locations_coordinates",
        ),
    )


class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"),
        primary_key=True,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )

    temperature_2m: Mapped[float] = mapped_column(Float, nullable=False)
    apparent_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    relative_humidity_2m: Mapped[float] = mapped_column(Float, nullable=False)
    precipitation: Mapped[float] = mapped_column(Float, nullable=False)
    precipitation_probability: Mapped[float] = mapped_column(Float, nullable=False)
    weather_code: Mapped[int] = mapped_column(Integer, nullable=False)
    cloud_cover: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed_10m: Mapped[float] = mapped_column(Float, nullable=False)
    wind_direction_10m: Mapped[float] = mapped_column(Float, nullable=False)
    wind_gusts_10m: Mapped[float] = mapped_column(Float, nullable=False)

    location: Mapped[Location] = relationship(back_populates="observations")

    __table_args__ = (
        CheckConstraint(
            "relative_humidity_2m BETWEEN 0 AND 100",
            name="ck_weather_observations_humidity",
        ),
        CheckConstraint(
            "precipitation >= 0",
            name="ck_weather_observations_precipitation",
        ),
        CheckConstraint(
            "precipitation_probability BETWEEN 0 AND 100",
            name="ck_weather_observations_precipitation_probability",
        ),
        CheckConstraint(
            "cloud_cover BETWEEN 0 AND 100",
            name="ck_weather_observations_cloud_cover",
        ),
        CheckConstraint(
            "wind_speed_10m >= 0",
            name="ck_weather_observations_wind_speed",
        ),
        CheckConstraint(
            "wind_direction_10m BETWEEN 0 AND 360",
            name="ck_weather_observations_wind_direction",
        ),
        CheckConstraint(
            "wind_gusts_10m >= 0",
            name="ck_weather_observations_wind_gusts",
        ),
    )
