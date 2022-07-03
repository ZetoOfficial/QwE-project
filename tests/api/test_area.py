import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.usefixtures("api_client")


async def test_areas(api_client: AsyncClient):
    response = await api_client.get(f"/api/areas?limit={0}&offset={0}")
    assert response.status_code == 200
    response = await api_client.get(f"/api/areas?limit={10}&offset={0}")
    assert response.status_code == 200


async def test_color_regions(api_client: AsyncClient):
    response = await api_client.get(f"/api/color_regions")
    assert response.status_code == 200
