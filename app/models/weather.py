"""Weather data models."""

from pydantic import BaseModel, Field


class DailyForecast(BaseModel):
    """Represents the daily weather forecast."""

    fecha: str = Field(..., json_schema_extra={"example": "2025-10-14"})
    temperatura_max: float
    temperatura_min: float
    probabilidad_precipitacion: int


class WeatherResponse(BaseModel):
    """Represents the weather response."""

    ubicacion: str
    latitud: float
    longitud: float
    temperatura_actual: float | None = None
    humedad_relativa: int | None = None
    pronostico_proximos_dias: list[DailyForecast]
    mensaje_info: str
