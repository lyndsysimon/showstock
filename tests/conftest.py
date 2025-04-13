"""
Test fixtures for the Showstock application.
"""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
from unittest.mock import patch, AsyncMock

from showstock.db import Base, get_db
from showstock.models import Brand, Feed, FeedType
from showstock.main import app


# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_engine():
    """Create a test engine using SQLite."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session_factory(test_engine):
    """Create a session factory for testing."""
    return sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )


@pytest_asyncio.fixture
async def async_session(async_session_factory):
    """Create a SQLAlchemy async session for testing with a fresh database."""
    async with async_session_factory() as session:
        yield session
        # Roll back all changes after each test
        await session.rollback()


@pytest.fixture
def override_get_db(async_session):
    """Override the get_db dependency."""
    async def _override_get_db():
        yield async_session
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()
