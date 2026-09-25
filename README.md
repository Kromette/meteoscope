# MeteoScope 🌦️

**MeteoScope** is a data science project dedicated to the exploration and analysis of meteorological time series.

The project combines **data engineering, backend development, statistical analysis, time-series modeling and interactive visualization** around real-world weather data.

> **MeteoScope — Exploring weather through data, statistics and time series.**

---

## 🚧 Project Status

**Early development — MVP in progress**

The project currently focuses on building a reliable foundation for collecting, storing and serving historical meteorological observations.

The first backend pipeline is operational:

```text
Open-Meteo
    ↓
Python ingestion
    ↓
PostgreSQL
    ↓
FastAPI
```

The current MVP supports:

- location search through the Open-Meteo geocoding API
- historical hourly weather observations
- PostgreSQL persistence
- idempotent data ingestion
- automatic retrieval of missing or incomplete historical data
- REST API access to observations
- automated tests and CI checks

Data transformation with dbt, statistical analysis, time-series modeling and the interactive frontend are planned for subsequent stages.

---

## 🎯 Project Goals

MeteoScope aims to provide an interactive environment for:

- exploring historical weather data
- visualizing meteorological time series
- computing descriptive statistics
- identifying trends, seasonality and anomalies
- studying relationships between meteorological variables
- experimenting with time-series analysis and forecasting
- eventually evaluating weather forecast performance

The objective is not to build another simple weather dashboard, but to use meteorological data as a practical foundation for **data engineering and data science work**.

---

## 🏗️ Architecture

The current architecture is intentionally kept simple and progressive.

```text
                         ┌───────────────┐
                         │   Open-Meteo  │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Python API    │
                         │ & ingestion   │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌────────────────┐
                         │   PostgreSQL   │
                         │                │
                         │ Locations      │
                         │ Observations   │
                         └───────┬────────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    FastAPI    │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ React frontend│
                         └───────────────┘
```

The project is designed to evolve progressively toward a larger analytical architecture:

```text
Open-Meteo
    ↓
Data ingestion
    ↓
PostgreSQL
    ↓
dbt transformations
    ↓
Analytical datasets
    ↓
Python data science
    ↓
FastAPI
    ↓
Interactive frontend
```

The main principle is to keep **data transformation** and **scientific analysis** conceptually distinct.

- **PostgreSQL** provides persistent storage for the operational weather data.
- **dbt** will later prepare clean, consistent and reusable analytical datasets.
- **Python** will be used for statistical analysis, feature engineering and time-series modeling.
- **FastAPI** exposes data and analytical capabilities to the frontend.
- **React** provides the interactive exploration interface.

---

## 🔄 Data Pipeline

The current pipeline is organized around several clearly separated responsibilities:

```text
Open-Meteo
    ↓
OpenMeteoClient
    ↓
Parser / validation
    ↓
WeatherIngestionService
    ↓
PostgreSQL
    ↓
FastAPI services
    ↓
REST API
```

### 1. Data ingestion

Meteorological data are retrieved from the Open-Meteo API and stored in PostgreSQL.

The ingestion layer is responsible for:

- retrieving historical weather observations
- normalizing API responses
- validating incoming data
- handling timestamps and time zones
- storing location metadata
- persisting hourly observations
- avoiding duplicate locations and observations
- making ingestion idempotent

The current MVP retrieves the **previous seven days of historical hourly observations**.

Forecast data are intentionally not stored at this stage.

### 2. Data persistence

PostgreSQL stores the operational weather dataset.

The current model is centered around two entities:

```text
locations
    │
    └── 1 → N
          weather_observations
```

A location is identified by its coordinates, while each weather observation is associated with a location and timestamp.

The database enforces important integrity constraints, including uniqueness of:

```text
(latitude, longitude)
```

and:

```text
(location_id, timestamp)
```

This allows the ingestion process to safely be executed multiple times without creating duplicate records.

### 3. API layer

FastAPI provides a stable interface between the frontend, database and external weather provider.

The API currently exposes:

```text
GET /health

GET /locations/search

GET /observations
```

The `/observations` endpoint retrieves observations for a requested location and date.

If the requested data are missing or incomplete, the backend can trigger the ingestion pipeline before reading the observations again from PostgreSQL.

This keeps the external API interaction inside the ingestion layer rather than coupling the frontend directly to Open-Meteo.

### 4. Analytical transformation

The next stage will introduce **dbt** to transform operational weather data into analytical datasets.

The intended direction is:

```text
weather_observations
        ↓
stg_weather_observations
        ↓
fct_weather_daily
        ↓
fct_weather_monthly
        ↓
fct_weather_yearly
```

These transformations may include:

- type normalization
- data quality checks
- unit consistency
- daily/monthly/yearly aggregations
- reusable analytical metrics

---

## 📊 Current Data Model

The MVP currently focuses on hourly historical weather observations.

The main meteorological variables include:

- temperature
- apparent temperature
- relative humidity
- precipitation
- precipitation probability
- weather code
- cloud cover
- wind speed
- wind direction
- wind gusts

Location metadata include information such as:

- latitude
- longitude
- timezone
- elevation

Weather observations are stored at **hourly resolution**, providing the foundation for future daily, monthly and yearly analytical datasets.

Missing values are represented explicitly rather than silently replaced.

---

## 🔬 Time-Series Analysis

One of the main objectives of MeteoScope is to use weather data as a practical case study for time-series analysis.

This work has not yet been implemented in the MVP and will be introduced progressively.

### Descriptive analysis

Planned analyses include:

- mean
- median
- variance
- standard deviation
- quantiles
- minimum / maximum
- distributions

### Temporal analysis

Planned analyses include:

- daily and monthly aggregation
- rolling statistics
- long-term trends
- seasonal patterns
- year-over-year comparisons

### Anomaly analysis

Meteorological observations can eventually be compared against historical reference periods to identify unusually warm, cold, wet or dry periods.

### Time-series modeling

Later stages may include:

- seasonal decomposition
- ACF / PACF analysis
- statistical forecasting models
- baseline forecasting
- forecast evaluation
- machine learning models

---

## 🌐 API

The backend is implemented with **FastAPI**.

Current endpoints:

```text
GET /health
GET /locations/search
GET /observations
```

The backend acts as an abstraction layer between the frontend, PostgreSQL and external data providers.

This allows the application to:

- centralize data retrieval
- normalize external API responses
- persist weather data
- validate API inputs
- reuse the ingestion pipeline
- expose a stable contract to the frontend
- progressively integrate analytical functionality

The API is documented automatically through FastAPI's OpenAPI integration.

---

## 🖥️ Frontend

The frontend is built with React and TypeScript.

It will provide an interactive interface for exploring weather data.

Planned capabilities include:

- location search
- historical data exploration
- interactive time-series charts
- statistical summaries
- trend visualization
- anomaly visualization

Additional weather-oriented features such as current conditions and forecast visualization may be added later.

The frontend is designed as an **exploration interface**, rather than only a presentation dashboard.

---

## 🛠️ Tech Stack

### Data source

- [Open-Meteo](https://open-meteo.com/)

### Backend

- Python
- FastAPI
- Pydantic
- HTTPX
- SQLAlchemy
- Alembic
- Uvicorn

### Database

- PostgreSQL
- Docker
- Docker Compose

### Data science & analytics

Planned:

- dbt
- pandas
- NumPy
- SciPy
- Statsmodels
- scikit-learn

### Frontend

- React
- TypeScript
- Vite
- pnpm

Planned / to be integrated:

- TanStack Query
- Plotly.js

### Development & quality

- uv
- Ruff
- Mypy
- pytest
- ESLint
- Prettier
- GitHub Actions

---

## 📁 Project Structure

The project is organized as a monorepo:

```text
meteoscope/

├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── src/
│   │   └── meteoscope/
│   │       ├── api/
│   │       ├── database/
│   │       ├── ingestion/
│   │       ├── services/
│   │       ├── config.py
│   │       └── main.py
│   │
│   └── tests/
│
├── frontend/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── docker-compose.yml
├── README.md
├── LICENSE
├── pyproject.toml
├── package.json
└── pnpm-workspace.yaml
```

The structure will evolve as the analytical and frontend layers are progressively implemented.

---

## 🧪 Testing & Quality

Testing is treated as part of the architecture rather than as a final step.

The backend currently includes tests covering:

- Open-Meteo API communication
- response parsing
- ingestion services
- database persistence
- ingestion idempotence
- API validation
- API behavior for missing or incomplete data

The project also uses automated quality checks:

```text
Ruff
Mypy
pytest
ESLint
Prettier
GitHub Actions
```

The CI pipeline validates the backend and frontend automatically.

---

## 🗺️ Roadmap

### Phase 1 — Backend & Data Pipeline

- [x] Repository initialization
- [x] Docker / PostgreSQL setup
- [x] Database migrations with Alembic
- [x] Open-Meteo API client
- [x] Historical weather ingestion
- [x] Data validation and parsing
- [x] Idempotent persistence
- [x] Location search
- [x] Historical observations API
- [x] API validation
- [x] Backend automated tests
- [x] CI quality checks
- [ ] Final API contract and documentation review

### Phase 2 — Interactive MVP

- [ ] React application foundation
- [ ] Location search interface
- [ ] Historical weather exploration
- [ ] Interactive time-series visualizations
- [ ] Basic statistical summaries
- [ ] Frontend/API integration
- [ ] End-to-end application validation

### Phase 3 — Analytics Engineering

- [ ] dbt integration
- [ ] Staging models
- [ ] Analytical data models
- [ ] Daily / monthly / yearly datasets
- [ ] Data quality tests
- [ ] Reusable analytical metrics

### Phase 4 — Time-Series Analysis

- [ ] Rolling statistics
- [ ] Historical climatology
- [ ] Anomalies relative to climatology
- [ ] Seasonal analysis
- [ ] Time-series decomposition
- [ ] ACF / PACF analysis
- [ ] Comparison between locations

### Phase 5 — Forecasting

- [ ] Forecasting baselines
- [ ] Statistical time-series models
- [ ] Forecast evaluation
- [ ] Error analysis by forecast horizon
- [ ] Comparison of forecasting approaches

### Phase 6 — Machine Learning

- [ ] Feature engineering
- [ ] Regression models
- [ ] Random Forest / Gradient Boosting
- [ ] Model evaluation
- [ ] Comparison with statistical baselines

### Phase 7 — Historical Forecast Analysis

- [ ] Store historical forecast runs
- [ ] Compare forecasts with observed data
- [ ] Analyze forecast error by horizon
- [ ] Study forecast performance across variables and locations

---

## 📚 Data Source & Licensing

MeteoScope initially uses Open-Meteo as its primary weather data provider.

Open-Meteo provides weather data from multiple meteorological models and open-data sources. Data obtained through the Open-Meteo API are provided under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** licence. Appropriate attribution to Open-Meteo is therefore required when using or redistributing the data.

For the purposes of this project, Open-Meteo is used through its free API for non-commercial use. The free service is subject to API usage limits. Commercial use requires an appropriate Open-Meteo subscription.

MeteoScope does not redistribute Open-Meteo's raw datasets as part of its source code. Weather data retrieved during development or execution are stored and processed separately from the application source code.

The MeteoScope source code is distributed under the **MIT License**. This licence applies only to the project's original source code and does not replace or modify the licences and attribution requirements applicable to data obtained from Open-Meteo or its underlying data sources.

For the latest terms and licensing information, see the [Open-Meteo Terms of Use](https://open-meteo.com/en/terms).

---

## 🚀 Long-Term Vision

MeteoScope is intended to evolve from an interactive weather exploration tool into a broader **meteorological time-series analysis platform**.

The long-term goal is to investigate questions such as:

- How do temperature trends evolve over time?
- How unusual is a given weather event compared with historical conditions?
- How strong are seasonal patterns for different variables?
- How do weather variables interact with each other?
- How accurately can future observations be predicted?
- How does forecast accuracy change with prediction horizon?
- How do these characteristics differ between locations?

The project is designed to make these questions accessible through a combination of **data engineering, statistical analysis, time-series modeling and interactive visualization**.
