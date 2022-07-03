import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.service import app
from settings import load_settings


@pytest_asyncio.fixture
async def api_client():
    settings = load_settings()
    async with AsyncClient(app=app, base_url=settings.app.service_host) as client:
        yield client
