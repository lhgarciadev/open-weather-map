"""Configuration settings for the application."""

from functools import lru_cache
import os


class Settings:
    """Application settings."""

    def __init__(self):
        """Initializes the settings."""
        self.OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")


@lru_cache
def get_settings() -> Settings:
    """Returns the cached settings object."""
    return Settings()
