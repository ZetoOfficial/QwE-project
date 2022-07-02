from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from settings import load_settings

app = FastAPI()
settings = load_settings()

if settings.app.origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.app.endpoint)
