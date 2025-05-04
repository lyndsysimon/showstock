"""
Feed-related models for the Showstock application.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from showstock.db import Base


class FeedType(str, enum.Enum):
    """Enum for feed types."""

    PELLET = "pellet"
    PULVERIZED = "pulverized"


class Brand(Base):
    """Brand model for feed manufacturers."""

    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    # Relationship to Feed model
    feeds = relationship("Feed", back_populates="brand")

    def __repr__(self):
        return f"<Brand(id={self.id}, name='{self.name}')>"


class Feed(Base):
    """Feed model for animal feed products."""

    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    name = Column(String, nullable=False)
    density = Column(Float, nullable=True)
    feed_type = Column(Enum(FeedType), nullable=False)
    weight = Column(Float, nullable=True)
    cost = Column(Float, nullable=True)

    # Relationship to Brand model
    brand = relationship("Brand", back_populates="feeds")

    def __repr__(self):
        return f"<Feed({self.id}, '{self.name}', brand={self.brand_id})>"
