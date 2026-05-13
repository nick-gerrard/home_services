import asyncio
import logging
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import settings
from services.subway import get_arrivals
from services.weather import get_weather

logger = logging.getLogger(__name__)

router = APIRouter()

_templates = Environment(
    loader=FileSystemLoader(str(Path(__file__).parent.parent / "templates")),
    autoescape=select_autoescape(["html"]),
)


async def _fetch_subway() -> list[dict]:
    try:
        return await get_arrivals(settings.subway_stop_id, settings.subway_line)
    except Exception:
        logger.exception("Subway fetch failed")
        return []


async def _fetch_weather() -> dict | None:
    try:
        return await get_weather(settings.default_latitude, settings.default_longitude)
    except Exception:
        logger.exception("Weather fetch failed")
        return None


@router.get("/dashboard")
async def dashboard(preview: bool = False):
    arrivals, weather = await asyncio.gather(_fetch_subway(), _fetch_weather())

    context = {"arrivals": arrivals, "weather": weather}
    template = "preview.html" if preview else "trmnl.html"
    html = _templates.get_template(template).render(**context)

    if preview:
        return HTMLResponse(html)
    return JSONResponse({"markup": html})
