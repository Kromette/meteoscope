### Location and Weather API Contract

The API separates **location discovery** from **weather data retrieval**.

- `GET /locations/search?q={query}` is used to search for cities through the Open-Meteo Geocoding API. Search results are transient and do not create database records.
- When a city is selected, the frontend requests weather observations using its **latitude and longitude**:
  `GET /observations?latitude={latitude}&longitude={longitude}&date={date}`
- The `location_id` is an internal MeteoScope identifier and is only created once the location is persisted in the database. It is therefore not required for the initial weather request.
- The backend first checks PostgreSQL for the requested location and date.
- If the location or the requested observations are missing, the backend fetches the required data from Open-Meteo, persists it, and returns the observations.
- PostgreSQL therefore acts as a **persistent cache**, while the backend remains responsible for deciding when external data must be fetched.
- Weather observations remain linked to the persisted location through the internal `location_id`.

This approach keeps the frontend independent from internal database identifiers while allowing MeteoScope to progressively persist locations as users select them.
