from datetime import UTC, datetime

import requests
from fastapi import HTTPException

from app.models.weather import DailyForecast, WeatherResponse


class OpenMeteoService:
    """
    A service class to interact with the Open-Meteo API.
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, latitude: float, longitude: float, city: str | None = None):
        self.latitude = latitude
        self.longitude = longitude
        self.city = city

    def get_weather_forecast(self) -> WeatherResponse:
        """
        Fetches and processes the weather forecast from Open-Meteo API.
        """
        try:
            params = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "hourly": "temperature_2m,relative_humidity_2m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "timezone": "auto",
                "temperature_unit": "celsius",
            }
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return self._prepare_response(data)
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to connect to Open-Meteo API: {e}"
            ) from e
        except (KeyError, TypeError) as e:
            raise HTTPException(status_code=500, detail=f"Error in data mapping: {e}") from e

    def _prepare_response(self, data: dict) -> WeatherResponse:
        """
        Maps the API response to the WeatherResponse model.
        """
        now = datetime.now(UTC)
        current_hour_index = now.hour

        current_temp = data["hourly"]["temperature_2m"][current_hour_index]
        current_humidity = data["hourly"]["relative_humidity_2m"][current_hour_index]

        daily_forecasts = []
        for i in range(len(data["daily"]["time"])):
            daily_forecasts.append(
                DailyForecast(
                    fecha=data["daily"]["time"][i],
                    temperatura_max=data["daily"]["temperature_2m_max"][i],
                    temperatura_min=data["daily"]["temperature_2m_min"][i],
                    probabilidad_precipitacion=data["daily"]["precipitation_probability_max"][i],
                )
            )

        location = self.city if self.city else f"{self.latitude}, {self.longitude}"

        return WeatherResponse(
            ubicacion=location,
            latitud=self.latitude,
            longitud=self.longitude,
            temperatura_actual=current_temp,
            humedad_relativa=current_humidity,
            pronostico_proximos_dias=daily_forecasts,
            mensaje_info=f"7-day weather forecast for {location}.",
        )
