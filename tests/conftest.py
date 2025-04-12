import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text
from typing import Generator, AsyncGenerator

from showstock.db import Base, get_db
from showstock.main import app
from showstock.config import settings

# Create a test database URL using environment variables from docker-compose
# Use a custom format for asyncpg to avoid the leading slash issue
TEST_DATABASE_URL = f"postgresql+asyncpg://{settings.db.USER}:{settings.db.PASSWORD}@{settings.db.HOST}:{settings.db.PORT}/showstock_test"

# Use the default event loop provided by pytest-asyncio
# We're not redefining it here to avoid conflicts


@pytest.fixture(scope="function")
async def engine():
    """Create a test database engine."""
    # Manually construct connection URL to ensure correct format for asyncpg
    url = f"postgresql+asyncpg://{settings.db.USER}:{settings.db.PASSWORD}@{settings.db.HOST}:{settings.db.PORT}/showstock_test"

    # Create async engine
    engine = create_async_engine(
        url,
        echo=True,
        pool_pre_ping=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db(engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for a test."""
    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async with async_session_factory() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture
async def client() -> Generator[TestClient, None, None]:
    """Create a test client with a test database dependency."""

    # Create a custom async generator for the get_db dependency
    async def override_get_db():
        # Manually construct connection URL to ensure correct format for asyncpg
        url = f"postgresql+asyncpg://{settings.db.USER}:{settings.db.PASSWORD}@{settings.db.HOST}:{settings.db.PORT}/showstock_test"

        test_engine = create_async_engine(
            url,
            echo=True,
            pool_pre_ping=True,
        )

        test_session_factory = async_sessionmaker(
            test_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

        async with test_session_factory() as session:
            try:
                yield session
            finally:
                await session.rollback()
                await session.close()

        await test_engine.dispose()

    # Override the get_db dependency
    app.dependency_overrides[get_db] = override_get_db

    # Use TestClient as a context manager
    with TestClient(app) as test_client:
        yield test_client

    # Reset the dependency override after the test is done
    app.dependency_overrides = {}
