"""
Tests for the database models.
"""

import pytest
from sqlalchemy import select

from showstock.models import Brand, Feed, FeedType


@pytest.mark.asyncio
async def test_create_brand(async_session):
    """Test creating a brand."""
    # Create a brand
    brand = Brand(name="Test Brand")
    async_session.add(brand)
    await async_session.commit()
    
    # Query the brand
    result = await async_session.execute(select(Brand).filter(Brand.name == "Test Brand"))
    db_brand = result.scalar_one()
    
    # Check the brand
    assert db_brand.id is not None
    assert db_brand.name == "Test Brand"


@pytest.mark.asyncio
async def test_create_feed(async_session):
    """Test creating a feed."""
    # Create a brand first
    brand = Brand(name="Test Brand")
    async_session.add(brand)
    await async_session.commit()
    
    # Create a feed
    feed = Feed(
        brand_id=brand.id,
        name="Test Feed",
        density=1.5,
        feed_type=FeedType.PELLET,
        weight=50.0,
        cost=25.99
    )
    async_session.add(feed)
    await async_session.commit()
    
    # Query the feed
    result = await async_session.execute(select(Feed).filter(Feed.name == "Test Feed"))
    db_feed = result.scalar_one()
    
    # Check the feed
    assert db_feed.id is not None
    assert db_feed.name == "Test Feed"
    assert db_feed.brand_id == brand.id
    assert db_feed.density == 1.5
    assert db_feed.feed_type == FeedType.PELLET
    assert db_feed.weight == 50.0
    assert db_feed.cost == 25.99


@pytest.mark.asyncio
async def test_brand_feed_relationship(async_session):
    """Test the relationship between brand and feed."""
    # Create a brand
    brand = Brand(name="Test Brand")
    async_session.add(brand)
    await async_session.commit()
    
    # Create feeds for the brand
    feed1 = Feed(
        brand_id=brand.id,
        name="Test Feed 1",
        feed_type=FeedType.PELLET
    )
    feed2 = Feed(
        brand_id=brand.id,
        name="Test Feed 2",
        feed_type=FeedType.PULVERIZED
    )
    async_session.add_all([feed1, feed2])
    await async_session.commit()
    
    # Query the feeds for the brand
    result = await async_session.execute(
        select(Feed).filter(Feed.brand_id == brand.id)
    )
    feeds = result.scalars().all()
    
    # Check the feeds
    assert len(feeds) == 2
    assert any(feed.name == "Test Feed 1" for feed in feeds)
    assert any(feed.name == "Test Feed 2" for feed in feeds)