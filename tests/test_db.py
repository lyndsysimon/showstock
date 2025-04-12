"""
Tests for the database connection utility.
"""

import os
import pytest
from unittest.mock import patch, AsyncMock, ANY

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from showstock.config import Settings, DatabaseSettings
from showstock.db import get_db, get_db_session, init_db, close_db


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch("showstock.db.settings") as mock_settings:
        db_settings = DatabaseSettings(
            HOST="test-host",
            PORT=5432,
            USER="test-user",
            PASSWORD="test-password",
            NAME="test-db",
            POOL_SIZE=2,
            MAX_OVERFLOW=5,
            ECHO=False,
        )
        mock_settings.db = db_settings
        yield mock_settings


@pytest.fixture
def mock_engine():
    """Mock SQLAlchemy engine for testing."""
    with patch("showstock.db.engine") as mock_engine:
        mock_engine.begin.return_value.__aenter__.return_value = AsyncMock()
        mock_engine.dispose = AsyncMock()
        yield mock_engine


@pytest.fixture
def mock_session_factory():
    """Mock SQLAlchemy session factory for testing."""
    with patch("showstock.db.async_session_factory") as mock_factory:
        mock_session = AsyncMock(spec=AsyncSession)
        mock_factory.return_value = mock_session
        yield mock_factory, mock_session


@pytest.mark.asyncio
async def test_init_db(mock_engine):
    """Test database initialization."""
    # Mock connection and cursor
    mock_conn = mock_engine.begin.return_value.__aenter__.return_value
    mock_conn.execute = AsyncMock()

    # Call the function
    await init_db()

    # Verify the connection was tested
    mock_conn.execute.assert_called_once_with(ANY)
    # Get the actual argument passed to execute
    actual_arg = mock_conn.execute.call_args[0][0]
    # Verify it's a TextClause with the correct SQL
    assert str(actual_arg) == "SELECT 1"


@pytest.mark.asyncio
async def test_init_db_exception_debug_mode(mock_settings, mock_engine):
    """Test database initialization with exception in debug mode."""
    # Set DEBUG to True
    mock_settings.DEBUG = True

    # Make the connection raise an exception
    mock_engine.begin.side_effect = Exception("Test connection error")

    # Call the function - should not raise an exception in debug mode
    await init_db()

    # No assertions needed - we're just verifying it doesn't raise an exception


@pytest.mark.asyncio
async def test_init_db_exception_production_mode(mock_settings, mock_engine):
    """Test database initialization with exception in production mode."""
    # Set DEBUG to False
    mock_settings.DEBUG = False

    # Make the connection raise an exception
    mock_engine.begin.side_effect = Exception("Test connection error")

    # Call the function - should raise an exception in production mode
    with pytest.raises(Exception, match="Test connection error"):
        await init_db()


@pytest.mark.asyncio
async def test_close_db(mock_engine):
    """Test database connection closing."""
    await close_db()
    mock_engine.dispose.assert_called_once()


@pytest.mark.asyncio
async def test_get_db(mock_session_factory):
    """Test the get_db dependency."""
    mock_factory, mock_session = mock_session_factory

    # Use the generator
    db_gen = get_db()
    session = await anext(db_gen)

    # Verify we got the session
    assert session == mock_session

    # Test exception handling
    mock_session.close = AsyncMock()
    mock_session.rollback = AsyncMock()

    # Simulate an exception during usage
    with patch("showstock.db.async_session_factory") as mock_factory:
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.close = AsyncMock()
        mock_session.rollback = AsyncMock()
        mock_factory.return_value = mock_session

        # Create a context that will raise an exception
        async def test_exception():
            async with get_db_session() as session:
                raise ValueError("Test exception")

        # Verify exception handling
        with pytest.raises(ValueError):
            await test_exception()

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()
