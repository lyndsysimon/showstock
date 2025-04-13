"""
API routes for the Showstock application.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel

from showstock.db import get_db
from showstock.models import Brand, Feed, FeedType

# Create API router
router = APIRouter(prefix="/api", tags=["api"])


# Pydantic models for request/response
class BrandCreate(BaseModel):
    name: str


class BrandResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class FeedCreate(BaseModel):
    brand_id: int
    name: str
    density: Optional[float] = None
    feed_type: FeedType
    weight: Optional[float] = None
    cost: Optional[float] = None


class FeedResponse(BaseModel):
    id: int
    brand_id: int
    name: str
    density: Optional[float] = None
    feed_type: FeedType
    weight: Optional[float] = None
    cost: Optional[float] = None

    class Config:
        from_attributes = True


# Brand endpoints
@router.post("/brands", response_model=BrandResponse, status_code=201)
async def create_brand(brand: BrandCreate, db: AsyncSession = Depends(get_db)):
    """Create a new brand."""
    db_brand = Brand(name=brand.name)
    db.add(db_brand)
    await db.commit()
    await db.refresh(db_brand)
    return db_brand


@router.get("/brands", response_model=List[BrandResponse])
async def get_brands(db: AsyncSession = Depends(get_db)):
    """Get all brands."""
    result = await db.execute(select(Brand))
    brands = result.scalars().all()
    return brands


@router.get("/brands/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: int, db: AsyncSession = Depends(get_db)):
    """Get a brand by ID."""
    result = await db.execute(select(Brand).filter(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    if brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


# Feed endpoints
@router.post("/feeds", response_model=FeedResponse, status_code=201)
async def create_feed(feed: FeedCreate, db: AsyncSession = Depends(get_db)):
    """Create a new feed."""
    # Check if brand exists
    result = await db.execute(select(Brand).filter(Brand.id == feed.brand_id))
    brand = result.scalar_one_or_none()
    if brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Create feed
    db_feed = Feed(
        brand_id=feed.brand_id,
        name=feed.name,
        density=feed.density,
        feed_type=feed.feed_type,
        weight=feed.weight,
        cost=feed.cost
    )
    db.add(db_feed)
    await db.commit()
    await db.refresh(db_feed)
    return db_feed


@router.get("/feeds", response_model=List[FeedResponse])
async def get_feeds(db: AsyncSession = Depends(get_db)):
    """Get all feeds."""
    result = await db.execute(select(Feed))
    feeds = result.scalars().all()
    return feeds


@router.get("/feeds/{feed_id}", response_model=FeedResponse)
async def get_feed(feed_id: int, db: AsyncSession = Depends(get_db)):
    """Get a feed by ID."""
    result = await db.execute(select(Feed).filter(Feed.id == feed_id))
    feed = result.scalar_one_or_none()
    if feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")
    return feed