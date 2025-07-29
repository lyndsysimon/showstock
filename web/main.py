from pathlib import Path

from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from showstock.api import get_brands, get_feeds
from showstock.db import get_db, init_db, close_db
from showstock.main import app as api_app


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="Showstock Web")

# Mount the existing API under /api
app.mount("/api", api_app)


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await close_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    brands = await get_brands(db)
    feeds = await get_feeds(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "brands": brands, "feeds": feeds}
    )
