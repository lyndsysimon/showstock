# Database Connection Utility

This document explains how to use the database connection utility in the Showstock application.

## Configuration

The database connection is configured using environment variables. You can set these variables in your `.env` file or directly in your environment.

### Database Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SHOWSTOCK_DB_HOST` | Database host | `localhost` |
| `SHOWSTOCK_DB_PORT` | Database port | `5432` |
| `SHOWSTOCK_DB_USER` | Database username | `postgres` |
| `SHOWSTOCK_DB_PASSWORD` | Database password | `postgres` |
| `SHOWSTOCK_DB_NAME` | Database name | `showstock` |
| `SHOWSTOCK_DB_POOL_SIZE` | Connection pool size | `5` |
| `SHOWSTOCK_DB_MAX_OVERFLOW` | Maximum number of connections to overflow | `10` |
| `SHOWSTOCK_DB_POOL_TIMEOUT` | Timeout for acquiring a connection from the pool | `30` |
| `SHOWSTOCK_DB_POOL_RECYCLE` | Time in seconds to recycle connections | `1800` |
| `SHOWSTOCK_DB_ECHO` | Enable SQL query logging | `false` |

## Using the Database Connection

### In FastAPI Endpoints

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from showstock.db import get_db
from showstock.models import Item

@app.get("/items/{item_id}")
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Get an item by ID."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

### In Other Async Functions

```python
from showstock.db import get_db_session

async def process_items():
    """Process all items in the database."""
    async with get_db_session() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()
        
        # Process items...
        
        # Commit changes
        await session.commit()
```

## Connection Pooling

The database connection utility uses SQLAlchemy's connection pooling to efficiently manage database connections. The pool is configured with the following parameters:

- `pool_size`: The number of connections to keep open in the pool
- `max_overflow`: The maximum number of connections to create beyond the pool size
- `pool_timeout`: The number of seconds to wait before timing out on getting a connection from the pool
- `pool_recycle`: The number of seconds after which a connection is recycled
- `pool_pre_ping`: Enables connection health checks before using a connection from the pool

## Testing

When writing tests that interact with the database, you can use the provided test fixtures to mock the database connection:

```python
import pytest
from unittest.mock import patch, AsyncMock

@pytest.fixture
def mock_db_session():
    """Mock database session for testing."""
    with patch("showstock.database.get_db_session") as mock_session:
        session = AsyncMock()
        mock_session.return_value.__aenter__.return_value = session
        yield session

@pytest.mark.asyncio
async def test_get_item(mock_db_session):
    """Test getting an item."""
    # Set up mock return value
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = {"id": 1, "name": "Test Item"}
    
    # Call the function that uses the database
    result = await get_item(1, mock_db_session)
    
    # Assert the result
    assert result["id"] == 1
    assert result["name"] == "Test Item"
```