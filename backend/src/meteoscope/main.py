from fastapi import FastAPI

from meteoscope.api.routes.health import router as health_router
from meteoscope.api.routes.search_location import router as search_location_router

app = FastAPI(title="MeteoScope API")

app.include_router(health_router)
app.include_router(search_location_router, prefix="/location/search")