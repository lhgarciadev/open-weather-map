"""Weather API router."""

import logging

from fastapi import APIRouter, Query

from app.models.weather import WeatherResponse
from app.services.open_meteo import OpenMeteoService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/weather", response_model=WeatherResponse)
def get_colombia_weather_forecast(
    latitude: float = Query(..., examples=[4.6097]),
    longitude: float = Query(..., examples=[-74.0817]),
    city: str | None = Query(None, examples=["Bogota"]),
):
    """Fetches the 7-day weather forecast for any location in Colombia."""
    logger.info("Fetching weather for lat=%s, lon=%s, city=%s", latitude, longitude, city)
    service = OpenMeteoService(latitude=latitude, longitude=longitude, city=city)
    return service.get_weather_forecast()
