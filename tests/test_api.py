"""
Tests for the API endpoints.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.testclient import TestClient

from showstock.main import app
from showstock.models import Brand, Feed, FeedType


@pytest.mark.asyncio
async def test_create_brand(async_session: AsyncSession):
    """Test creating a brand via API."""
    client = TestClient(app)
    response = client.post(
        "/api/brands",
        json={"name": "Test Brand"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Brand"
    assert "id" in data

    # Verify in database
    result = await async_session.execute(select(Brand).filter(Brand.id == data["id"]))
    brand = result.scalar_one_or_none()
    assert brand is not None
    assert brand.name == "Test Brand"


@pytest.mark.asyncio
async def test_get_brands(async_session: AsyncSession):
    """Test getting all brands."""
    # Create test brands
    brand1 = Brand(name="Brand 1")
    brand2 = Brand(name="Brand 2")
    async_session.add_all([brand1, brand2])
    await async_session.commit()

    client = TestClient(app)
    response = client.get("/api/brands")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(brand["name"] == "Brand 1" for brand in data)
    assert any(brand["name"] == "Brand 2" for brand in data)


@pytest.mark.asyncio
async def test_get_brand(async_session: AsyncSession):
    """Test getting a brand by ID."""
    # Create test brand
    brand = Brand(name="Test Brand")
    async_session.add(brand)
    await async_session.commit()

    client = TestClient(app)
    response = client.get(f"/api/brands/{brand.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == brand.id
    assert data["name"] == "Test Brand"


@pytest.mark.asyncio
async def test_get_brand_not_found():
    """Test getting a non-existent brand."""
    client = TestClient(app)
    response = client.get("/api/brands/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Brand not found"


@pytest.mark.asyncio
async def test_create_feed(async_session: AsyncSession):
    """Test creating a feed."""
    # Create a brand first
    brand = Brand(name="Test Brand")
    async_session.add(brand)
    await async_session.commit()

    client = TestClient(app)
    response = client.post(
        "/api/feeds",
        json={
            "brand_id": brand.id,
            "name": "Test Feed",
            "density": 1.5,
            "feed_type": "pellet",
            "weight": 50.0,
            "cost": 25.99,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Feed"
    assert data["brand_id"] == brand.id
    assert data["density"] == 1.5
    assert data["feed_type"] == "pellet"
    assert data["weight"] == 50.0
    assert data["cost"] == 25.99

    # Verify in database
    result = await async_session.execute(select(Feed).filter(Feed.id == data["id"]))
    feed = result.scalar_one_or_none()
    assert feed is not None
    assert feed.name == "Test Feed"
    assert feed.brand_id == brand.id


@pytest.mark.asyncio
async def test_create_feed_invalid_brand():
    """Test creating a feed with an invalid brand ID."""
    client = TestClient(app)
    response = client.post(
        "/api/feeds",
        json={
            "brand_id": 999,
            "name": "Test Feed",
            "feed_type": "pellet",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Brand not found"


@pytest.mark.asyncio
async def test_get_feeds(async_session: AsyncSession):
    """Test getting all feeds."""
    # Create a brand
    brand = Brand(name="Test Brand")
    async_session.add(brand)
    await async_session.commit()

    # Create test feeds
    feed1 = Feed(
        brand_id=brand.id,
        name="Feed 1",
        feed_type=FeedType.PELLET,
    )
    feed2 = Feed(
        brand_id=brand.id,
        name="Feed 2",
        feed_type=FeedType.PULVERIZED,
    )
    async_session.add_all([feed1, feed2])
    await async_session.commit()

    client = TestClient(app)
    response = client.get("/api/feeds")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(feed["name"] == "Feed 1" for feed in data)
    assert any(feed["name"] == "Feed 2" for feed in data)


@pytest.mark.asyncio
async def test_get_feed(async_session: AsyncSession):
    """Test getting a feed by ID."""
    # Create a brand
    brand = Brand(name="Test Brand")
    async_session.add(brand)
    await async_session.commit()

    # Create test feed
    feed = Feed(
        brand_id=brand.id,
        name="Test Feed",
        feed_type=FeedType.PELLET,
    )
    async_session.add(feed)
    await async_session.commit()

    client = TestClient(app)
    response = client.get(f"/api/feeds/{feed.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feed.id
    assert data["name"] == "Test Feed"
    assert data["brand_id"] == brand.id


@pytest.mark.asyncio
async def test_get_feed_not_found():
    """Test getting a non-existent feed."""
    client = TestClient(app)
    response = client.get("/api/feeds/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Feed not found"