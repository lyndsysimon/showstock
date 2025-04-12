"""
Database connection utility for the Showstock application.
Provides a SQLAlchemy connection pool and session management.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy import text

from showstock.config import settings

# Configure logger
logger = logging.getLogger(__name__)

# SQLAlchemy declarative base
Base = declarative_base()

# Get database URL from settings
db_url = str(settings.db.DATABASE_URL)

# Create async SQLAlchemy engine with connection pooling
engine = create_async_engine(
    db_url,
    echo=settings.db.ECHO,
    pool_size=settings.db.POOL_SIZE,
    max_overflow=settings.db.MAX_OVERFLOW,
    pool_timeout=settings.db.POOL_TIMEOUT,
    pool_recycle=settings.db.POOL_RECYCLE,
    pool_pre_ping=True,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for database sessions.

    Yields:
        AsyncSession: SQLAlchemy async session

    Example:
        ```python
        async with get_db_session() as session:
            result = await session.execute(query)
            await session.commit()
        ```
    """
    session = async_session_factory()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        logger.exception(f"Database session error: {e}")
        raise
    finally:
        await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async generator for database sessions.

    Yields:
        AsyncSession: SQLAlchemy async session

    Example:
        ```python
        @app.get("/items/")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
        ```
    """
    async with get_db_session() as session:
        yield session


async def init_db() -> None:
    """Initialize database connection."""
    try:
        # Test connection by making a simple query
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        # In development mode, we might want to continue even if the database is not available
        if settings.DEBUG:
            logger.warning("Running in DEBUG mode without database connection")
        else:
            raise


async def close_db() -> None:
    """Close database connection pool."""
    await engine.dispose()
    logger.info("Database connection pool closed")
