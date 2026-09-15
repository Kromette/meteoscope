# MeteoScope 🌦️

**MeteoScope** is a data science project dedicated to the exploration and analysis of meteorological time series.

The project aims to go beyond a traditional weather application by combining **data engineering, analytics engineering, statistical analysis, time-series modeling and interactive visualization**.

> **MeteoScope — Exploring weather through data, statistics and time series.**

## 🚧 Project Status

**Early development — MVP in progress**

The project is currently focused on building a reliable data pipeline and an interactive foundation for exploring historical and forecast weather data.

---

## 🎯 Project Goals

MeteoScope aims to provide an interactive environment for:

- exploring current and historical weather data
- visualizing meteorological time series
- computing descriptive statistics
- identifying trends, seasonality and anomalies
- studying relationships between meteorological variables
- experimenting with time-series analysis and forecasting
- eventually evaluating forecast performance

The objective is not to build another simple weather dashboard, but to use meteorological data as a foundation for a **data science and time-series analysis project**.

---

## 🏗️ Architecture

MeteoScope follows a data-oriented architecture in which raw meteorological data are progressively transformed into analytical datasets before being used for scientific analysis and visualization.

```text
                         ┌───────────────┐
                         │   Open-Meteo  │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Data ingestion│
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │  Raw weather  │
                         │      data     │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │      dbt      │
                         │ Transformation│
                         └───────┬───────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Analytical datasets  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Python Data Science  │
                    │                         │
                    │ • Statistics            │
                    │ • Time-series analysis  │
                    │ • Feature engineering   │
                    │ • Forecasting           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Interactive exploration │
                    │   & visualization       │
                    └─────────────────────────┘
```

The main principle is to keep **data transformation** and **scientific analysis** conceptually distinct:

- **dbt** prepares clean, consistent and reusable analytical datasets from the raw data.
- **Python** is used for statistical and time-series analysis, feature engineering and, later, predictive modeling.
- The resulting analyses are exposed through the backend and visualized through the frontend.

---

## 🔄 Data Pipeline

The project is organized around a progressive data transformation pipeline:

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
Python analysis
    ↓
FastAPI
    ↓
Interactive frontend
```

### 1. Data ingestion

Meteorological data are retrieved from the Open-Meteo APIs and stored in PostgreSQL.

The ingestion layer is responsible for:

- retrieving weather data
- normalizing API responses
- handling timestamps and time zones
- storing raw weather observations
- avoiding unnecessary repeated API requests

### 2. Data transformation

dbt transforms the stored weather data into clean and reusable analytical datasets.

Potential models include:

```text
weather_hourly_raw
        ↓
stg_weather_hourly
        ↓
fct_weather_daily
        ↓
fct_weather_monthly
        ↓
fct_weather_yearly
```

These transformations can include:

- type normalization
- data quality checks
- timestamp normalization
- unit consistency
- daily/monthly/yearly aggregations
- reusable analytical metrics

### 3. Scientific analysis

Python operates on the analytical datasets produced by the transformation layer.

This layer will progressively support:

- descriptive statistics
- rolling statistics
- anomaly detection
- trend analysis
- seasonal analysis
- time-series decomposition
- autocorrelation analysis
- feature engineering
- forecasting models

---

## 📊 Initial Data

The MVP focuses on a subset of meteorological variables:

- temperature
- apparent temperature
- minimum and maximum temperature
- precipitation
- rain
- snow
- precipitation probability
- wind speed
- wind gusts
- wind direction
- atmospheric pressure
- relative humidity
- cloud cover

Additional variables such as radiation or UV-related measurements may be added later depending on the analytical use cases.

Weather data are stored at hourly resolution when available, allowing the project to derive daily, monthly and yearly datasets.

---

## 🔬 Time-Series Analysis

One of the main objectives of MeteoScope is to use weather data as a practical case study for time-series analysis.

Planned analyses include:

### Descriptive analysis

- mean
- median
- variance
- standard deviation
- quantiles
- minimum / maximum
- distributions

### Temporal analysis

- daily and monthly aggregation
- rolling mean and standard deviation
- long-term trends
- seasonal patterns
- year-over-year comparisons

### Anomaly analysis

Meteorological observations can be compared against historical reference periods to identify unusually warm, cold, wet or dry periods.

### Time-series modeling

Later stages of the project may include:

- seasonal decomposition
- ACF / PACF analysis
- statistical forecasting models
- baseline forecasting
- forecast evaluation
- machine learning models

---

## 🌐 API

The backend will expose the data and analytical capabilities through a REST API.

Initial endpoints are planned around:

```text
GET /locations/search
GET /weather/current
GET /weather/forecast
GET /weather/history
GET /weather/statistics
```

The backend acts as an abstraction layer between the frontend, the database and external data providers.

This allows the application to:

- centralize data retrieval
- normalize external API responses
- cache and persist data
- expose a stable API to the frontend
- progressively integrate analytical functionality

---

## 🖥️ Frontend

The frontend will provide an interactive interface for exploring weather data.

Planned capabilities include:

- location search
- current weather overview
- 7-day forecast
- historical data exploration
- interactive time-series charts
- statistical summaries
- trend and anomaly visualization

The frontend is designed as an exploration interface rather than only a presentation dashboard.

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

### Data & analytics

- PostgreSQL
- dbt
- pandas
- NumPy
- SciPy
- Statsmodels
- scikit-learn _(planned)_

### Frontend

- React
- TypeScript
- Vite
- TanStack Query
- Plotly.js
- pnpm

### Development & quality

- Docker
- Docker Compose
- pytest
- Ruff
- Mypy
- ESLint
- Prettier
- GitHub Actions

---

## 📁 Project Structure

The project is organized as a monorepo:

```text
meteoscope/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── analysis/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   └── tests/
│
├── frontend/
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── tests/
│   └── dbt_project.yml
│
├── notebooks/
├── data/
│
├── docker-compose.yml
├── README.md
├── LICENSE
└── .gitignore
```

The exact structure may evolve as the project grows.

---

## 🗺️ Roadmap

### Phase 1 — MVP

- [ ] Location search
- [ ] Current weather
- [ ] 7-day forecast
- [ ] Historical weather
- [ ] PostgreSQL storage
- [ ] Basic data ingestion pipeline
- [ ] dbt staging and analytical models
- [ ] Interactive time-series visualizations
- [ ] Descriptive statistics
- [ ] Basic trend analysis
- [ ] Basic anomaly analysis

### Phase 2 — Time-Series Analysis

- [ ] Daily / monthly / yearly analytical datasets
- [ ] Rolling statistics
- [ ] Historical climatology
- [ ] Anomalies relative to climatology
- [ ] Seasonal analysis
- [ ] Time-series decomposition
- [ ] ACF / PACF analysis
- [ ] Comparison between locations

### Phase 3 — Forecasting

- [ ] Forecasting baselines
- [ ] Statistical time-series models
- [ ] Forecast evaluation
- [ ] Error analysis by forecast horizon
- [ ] Comparison of forecasting approaches

### Phase 4 — Machine Learning

- [ ] Feature engineering
- [ ] Regression models
- [ ] Random Forest / Gradient Boosting
- [ ] Model evaluation
- [ ] Comparison with statistical baselines

### Phase 5 — Historical Forecast Analysis

- [ ] Store historical forecast runs
- [ ] Compare forecasts with observed/reanalysis data
- [ ] Analyze forecast error by horizon
- [ ] Study forecast performance across variables and locations

---

## 📚 Data Source & Licensing

MeteoScope initially uses Open-Meteo as its primary weather data provider.

Open-Meteo provides weather data from multiple meteorological models and open-data sources. Data obtained through the Open-Meteo API are provided under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence. Appropriate attribution to Open-Meteo is therefore required when using or redistributing the data.

For the purposes of this project, Open-Meteo is used through its free API for non-commercial use. The current free tier is subject to API usage limits, including limits on the number of requests per minute, hour and day. Commercial use requires an appropriate Open-Meteo subscription.

MeteoScope does not redistribute Open-Meteo's raw datasets as part of its source code. Weather data retrieved during development or execution are stored and processed separately from the application source code.

The MeteoScope source code is distributed under the MIT License. This licence applies only to the project's original source code and does not replace or modify the licences and attribution requirements applicable to data obtained from Open-Meteo or its underlying data sources.

For more information, see the Open-Meteo Terms of Use.

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
