from httpx import AsyncClient
import pytest
from app.main import app
from app.database import SessionLocal, init_db


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_order(client):
    order_data = {"user_id": 1, "items": [{"product_id": 101, "quantity": 2}]}
    response = await client.post("/orders/", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert len(data["items"]) == 1


@pytest.mark.asyncio
async def test_read_order(client):
    response = await client.get("/orders/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_update_order_status(client):
    response = await client.put("/orders/1/status", json={"status": "completed"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Order status updated"
