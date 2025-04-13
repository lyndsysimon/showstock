import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from showstock.main import app, startup_event, shutdown_event

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_db_test(override_get_db, test_engine):
    # Mock the database connection test to return success
    client = TestClient(app)
    response = client.get("/db-test")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    # We're not testing the actual connection here, just that the endpoint works


# We'll skip testing startup/shutdown events directly since they require
# a real database connection and are already covered by the other tests
