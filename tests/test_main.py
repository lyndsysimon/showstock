import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

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
    # Test the API endpoint
    client = TestClient(app)
    response = client.get("/db-test")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


@pytest.mark.asyncio
async def test_startup_event():
    """Test the startup event."""
    with patch("showstock.main.init_db") as mock_init_db:
        await startup_event()
        mock_init_db.assert_called_once()


@pytest.mark.asyncio
async def test_shutdown_event():
    """Test the shutdown event."""
    with patch("showstock.main.close_db") as mock_close_db:
        await shutdown_event()
        mock_close_db.assert_called_once()


@pytest.mark.asyncio
async def test_db_test_success():
    """Test the db_test function with a successful result."""
    from showstock.main import db_test

    # Create a real SQLite in-memory database session
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        result = await db_test(db=session)
        assert result["status"] == "connected"
        assert result["test_value"] == 1


@pytest.mark.asyncio
async def test_db_test_exception():
    """Test the db_test endpoint with an exception."""
    # Create a mock session that raises an exception
    mock_session = MagicMock()
    mock_session.execute.side_effect = Exception("Test exception")

    # Test the endpoint with the mocked session
    from showstock.main import db_test

    result = await db_test(db=mock_session)
    assert result["status"] == "error"
    assert "Test exception" in result["message"]
