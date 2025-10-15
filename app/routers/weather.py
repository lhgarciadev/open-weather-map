from fastapi import APIRouter, Query

from app.models.weather import WeatherResponse
from app.services.open_meteo import OpenMeteoService

router = APIRouter()


@router.get("/weather", response_model=WeatherResponse)
def get_colombia_weather_forecast(
    latitude: float = Query(..., examples=[4.6097]),
    longitude: float = Query(..., examples=[-74.0817]),
    city: str | None = Query(None, examples=["Bogota"]),
):
    """
    Fetches the 7-day weather forecast for any location in Colombia.
    """
    service = OpenMeteoService(latitude=latitude, longitude=longitude, city=city)
    return service.get_weather_forecast()
