"""Main application file."""

import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import APIDataMappingError, OpenMeteoAPIError
from app.core.logging_config import setup_logging
from app.routers import weather


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""
    # Setup logging
    setup_logging()

    # Get logger
    logger = logging.getLogger(__name__)
    settings = get_settings()

    # Conditionally disable docs
    app_kwargs = {
        "title": "Open Weather Map API",
        "description": (
            "Una API para obtener el pronóstico del tiempo para Colombia usando Open-Meteo."
        ),
        "version": "1.0.0",
    }
    if settings.ENVIRONMENT == "production":
        app_kwargs["docs_url"] = None
        app_kwargs["redoc_url"] = None
        app_kwargs["openapi_url"] = None

    app = FastAPI(**app_kwargs)

    @app.exception_handler(OpenMeteoAPIError)
    async def open_meteo_api_exception_handler(request, exc: OpenMeteoAPIError):
        logger.error("Error connecting to the external API: %s", exc.message)
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred with the external weather API: {exc.message}"},
        )

    @app.exception_handler(APIDataMappingError)
    async def data_mapping_exception_handler(request, exc: APIDataMappingError):
        logger.error("Error mapping data from the external API: %s", exc.message)
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred while processing weather data: {exc.message}"},
        )

    app.include_router(weather.router, prefix="/api/v1", tags=["Weather"])

    @app.get("/", tags=["Root"])
    def read_root():
        return {"message": "Welcome to the Open Weather Map API!"}

    return app


app = create_app()
