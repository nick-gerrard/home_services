import asyncio
import logging
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import settings
from services.subway import get_arrivals
from services.weather import get_weather
from services.xkcd import get_xkcd

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


async def _fetch_xkcd() -> dict | None:
    try:
        return await get_xkcd()
    except Exception:
        logger.exception("XKCD fetch failed")
        return None


@router.get("/dashboard")
async def dashboard(preview: bool = False):
    arrivals, weather, xkcd = await asyncio.gather(
        _fetch_subway(), _fetch_weather(), _fetch_xkcd()
    )

    if preview:
        html = _templates.get_template("preview.html").render(
            arrivals=arrivals, weather=weather, xkcd=xkcd
        )
        return HTMLResponse(html)

    return JSONResponse({"arrivals": arrivals, "weather": weather, "xkcd": xkcd})
