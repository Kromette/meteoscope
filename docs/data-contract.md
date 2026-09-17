# Meteoscope — Data Contract

## Purpose

Define the canonical weather data model between Open-Meteo, the Python ingestion pipeline, and PostgreSQL.

The reference granularity is **hourly**:

> One observation = one location + one timestamp.

## Location context

| Field       | Type   | Unit |
| ----------- | ------ | ---- |
| `latitude`  | float  | °    |
| `longitude` | float  | °    |
| `timezone`  | string | IANA |
| `elevation` | float  | m    |

The coordinates and timezone returned by Open-Meteo are kept as the reference for the retrieved data.

## Hourly observation

| Field                       | Type     | Unit |
| --------------------------- | -------- | ---- |
| `timestamp`                 | datetime | —    |
| `temperature_2m`            | float    | °C   |
| `apparent_temperature`      | float    | °C   |
| `relative_humidity_2m`      | float    | %    |
| `precipitation`             | float    | mm   |
| `precipitation_probability` | float    | %    |
| `weather_code`              | integer  | WMO  |
| `cloud_cover`               | float    | %    |
| `wind_speed_10m`            | float    | km/h |
| `wind_direction_10m`        | float    | °    |
| `wind_gusts_10m`            | float    | km/h |

## Main rules

- Hourly data is the **canonical source**; daily data can be derived from it.
- Units are kept as defined by the Open-Meteo request.
- `weather_code` is stored as a numeric WMO code; its human-readable representation belongs to the presentation layer.
- `wind_direction_10m` is stored in degrees; conversion to cardinal directions belongs to the presentation layer.
- Missing values are represented by `NULL`, never by artificial values.
- An observation must not be inserted more than once; uniqueness will be based on location and timestamp.
- Domain constraints are validated before insertion (percentages `0–100`, precipitation and wind speeds `≥ 0`, etc.).

## Out of scope

The following technical metadata is not part of the weather observation model:

- `generationtime_ms`
- `utc_offset_seconds`
- `timezone_abbreviation`
- `hourly_units`

`generationtime_ms` may still be used for observability and API performance monitoring.

## Evolution

The contract is intentionally limited to the MVP scope.

Any additional Open-Meteo variable must be explicitly added to this contract before being integrated into the data model.

## Database schema

locations
---------

id INTEGER PRIMARY KEY
latitude DOUBLE PRECISION NOT NULL
longitude DOUBLE PRECISION NOT NULL
timezone TEXT NOT NULL
elevation DOUBLE PRECISION NOT NULL

weather_observations
--------------------

location_id INTEGER NOT NULL
timestamp TIMESTAMPTZ NOT NULL
temperature_2m DOUBLE PRECISION NOT NULL
apparent_temperature DOUBLE PRECISION NOT NULL
relative_humidity_2m DOUBLE PRECISION NOT NULL
precipitation DOUBLE PRECISION NOT NULL
precipitation_probability DOUBLE PRECISION NOT NULL
weather_code INTEGER NOT NULL
cloud_cover DOUBLE PRECISION NOT NULL
wind_speed_10m DOUBLE PRECISION NOT NULL
wind_direction_10m DOUBLE PRECISION NOT NULL
wind_gusts_10m DOUBLE PRECISION NOT NULL

PRIMARY KEY (location_id, timestamp)
FOREIGN KEY (location_id) REFERENCES locations(id)
