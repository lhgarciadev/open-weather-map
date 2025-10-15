from fastapi import FastAPI

from app.routers import weather

app = FastAPI(
    title="Open Weather Map API",
    description="Una API para obtener el pronóstico del tiempo para Colombia usando Open-Meteo.",
    version="1.0.0",
)

app.include_router(weather.router, prefix="/api/v1", tags=["Weather"])


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Open Weather Map API!"}
