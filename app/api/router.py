from fastapi import APIRouter

from app.api.endpoints import area, chart, file, vacancy

api_router = APIRouter()

api_router.include_router(vacancy.router, tags=["vacancy"])
api_router.include_router(area.router, tags=["area"])
api_router.include_router(chart.router, prefix="/charts", tags=["chart"])
api_router.include_router(file.router, prefix="/files", tags=["file"])
