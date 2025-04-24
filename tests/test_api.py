"""
Tests for the API endpoints.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.testclient import TestClient

from showstock.main import app
from showstock.models import Brand, Feed, FeedType
from showstock.api import (
    create_brand,
    get_brands,
    get_brand,
    create_feed,
    get_feeds,
    get_feed,
)


@pytest.mark.asyncio
async def test_create_brand(async_session: AsyncSession, override_get_db):
    """Test creating a brand via API."""
    # Test the API endpoint
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
    query = select(Brand).filter(Brand.id == data["id"])
    result = await async_session.execute(query)
    brand = result.scalar_one_or_none()
    assert brand is not None
    assert brand.name == "Test Brand"

    # Test refresh functionality
    brand.name = "Updated Brand"
    await async_session.commit()
    await async_session.refresh(brand)
    assert brand.name == "Updated Brand"

    # Test the API function directly
    from showstock.api import BrandCreate

    brand_data = BrandCreate(name="Direct Test Brand")
    new_brand = await create_brand(brand_data, async_session)
    assert new_brand.name == "Direct Test Brand"
    assert new_brand.id is not None


@pytest.mark.asyncio
async def test_get_brands(async_session: AsyncSession, override_get_db):
    """Test getting all brands."""
    # Create test brands
    brand1 = Brand(name="Brand 1")
    brand2 = Brand(name="Brand 2")
    async_session.add_all([brand1, brand2])
    await async_session.commit()

    # Test the API endpoint
    client = TestClient(app)
    response = client.get("/api/brands")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(brand["name"] == "Brand 1" for brand in data)
    assert any(brand["name"] == "Brand 2" for brand in data)

    # Test the API function directly
    brands = await get_brands(async_session)
    assert len(brands) >= 2
    assert any(brand.name == "Brand 1" for brand in brands)
    assert any(brand.name == "Brand 2" for brand in brands)


@pytest.mark.asyncio
async def test_get_brand(async_session: AsyncSession, override_get_db):
    """Test getting a brand by ID."""
    # Create test brand
    brand = Brand(name="Test Brand")
    async_session.add(brand)
    await async_session.commit()

    # Test the API endpoint
    client = TestClient(app)
    response = client.get(f"/api/brands/{brand.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == brand.id
    assert data["name"] == "Test Brand"

    # Test the API function directly
    db_brand = await get_brand(brand.id, async_session)
    assert db_brand is not None
    assert db_brand.id == brand.id
    assert db_brand.name == "Test Brand"

    # Test not found case with API function
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as excinfo:
        await get_brand(9999, async_session)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Brand not found"


@pytest.mark.asyncio
async def test_get_brand_not_found(override_get_db):
    """Test getting a non-existent brand."""
    client = TestClient(app)
    response = client.get("/api/brands/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Brand not found"


@pytest.mark.asyncio
async def test_create_feed(async_session: AsyncSession, override_get_db):
    """Test creating a feed."""
    # Create a brand first
    brand = Brand(name="Test Brand")
    async_session.add(brand)
    await async_session.commit()

    # Test the API endpoint
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
    query = select(Feed).filter(Feed.id == data["id"])
    result = await async_session.execute(query)
    feed = result.scalar_one_or_none()
    assert feed is not None
    assert feed.name == "Test Feed"
    assert feed.brand_id == brand.id

    # Test refresh functionality
    feed.name = "Updated Feed"
    await async_session.commit()
    await async_session.refresh(feed)
    assert feed.name == "Updated Feed"

    # Test the API function directly
    from showstock.api import FeedCreate

    feed_data = FeedCreate(
        brand_id=brand.id,
        name="Direct Test Feed",
        density=2.0,
        feed_type=FeedType.PELLET,
        weight=75.0,
        cost=30.99,
    )
    new_feed = await create_feed(feed_data, async_session)
    assert new_feed.name == "Direct Test Feed"
    assert new_feed.brand_id == brand.id
    assert new_feed.density == 2.0
    assert new_feed.feed_type == FeedType.PELLET
    assert new_feed.weight == 75.0
    assert new_feed.cost == 30.99


@pytest.mark.asyncio
async def test_create_feed_invalid_brand(async_session: AsyncSession, override_get_db):
    """Test creating a feed with an invalid brand ID."""
    # Test the API endpoint
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

    # Test the API function directly
    from showstock.api import FeedCreate
    from fastapi import HTTPException

    feed_data = FeedCreate(
        brand_id=999,
        name="Direct Test Feed",
        feed_type=FeedType.PELLET,
    )
    with pytest.raises(HTTPException) as excinfo:
        await create_feed(feed_data, async_session)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Brand not found"


@pytest.mark.asyncio
async def test_get_feeds(async_session: AsyncSession, override_get_db):
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

    # Test the API endpoint
    client = TestClient(app)
    response = client.get("/api/feeds")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(feed["name"] == "Feed 1" for feed in data)
    assert any(feed["name"] == "Feed 2" for feed in data)

    # Test the API function directly
    feeds = await get_feeds(async_session)
    assert len(feeds) >= 2
    assert any(feed.name == "Feed 1" for feed in feeds)
    assert any(feed.name == "Feed 2" for feed in feeds)


@pytest.mark.asyncio
async def test_get_feed(async_session: AsyncSession, override_get_db):
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

    # Test the API endpoint
    client = TestClient(app)
    response = client.get(f"/api/feeds/{feed.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feed.id
    assert data["name"] == "Test Feed"
    assert data["brand_id"] == brand.id

    # Test the API function directly
    db_feed = await get_feed(feed.id, async_session)
    assert db_feed is not None
    assert db_feed.id == feed.id
    assert db_feed.name == "Test Feed"

    # Test not found case with API function
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as excinfo:
        await get_feed(9999, async_session)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Feed not found"


@pytest.mark.asyncio
async def test_get_feed_not_found(override_get_db):
    """Test getting a non-existent feed."""
    client = TestClient(app)
    response = client.get("/api/feeds/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Feed not found"
