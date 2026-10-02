from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from meteoscope.api.routes.health import router as health_router
from meteoscope.api.routes.marine import router as marine_router
from meteoscope.api.routes.observations import router as observations_router
from meteoscope.api.routes.search_location import router as search_location_router

app = FastAPI(title="MeteoScope API")

app.include_router(health_router)
app.include_router(search_location_router)
app.include_router(observations_router)
app.include_router(marine_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
