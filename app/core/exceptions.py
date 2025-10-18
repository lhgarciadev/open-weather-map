"""Custom exceptions for the application."""


class OpenMeteoError(Exception):
    """Base exception for errors related to the OpenMeteo service."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class OpenMeteoAPIError(OpenMeteoError):
    """Raised when the Open-Meteo API request fails."""


class APIDataMappingError(OpenMeteoError):
    """Raised when there is an error mapping API data."""
