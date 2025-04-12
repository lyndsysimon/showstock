from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from showstock.config import settings
from showstock.db import get_db, init_db, close_db

app = FastAPI(
    title=settings.APP_NAME, description=settings.APP_DESCRIPTION, debug=settings.DEBUG
)


@app.on_event("startup")
async def startup_event():
    """Initialize connections and resources on application startup."""
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Close connections and free resources on application shutdown."""
    await close_db()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": f"Welcome to {settings.APP_NAME} - {settings.APP_DESCRIPTION}"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/db-test")
async def db_test(db: AsyncSession = Depends(get_db)):
    """Test database connection."""
    try:
        result = await db.execute(text("SELECT 1 as test"))
        value = result.scalar()
        return {"status": "connected", "test_value": value}
    except Exception as e:
        return {"status": "error", "message": str(e)}
