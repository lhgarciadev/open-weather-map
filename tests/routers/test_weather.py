from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_colombia_weather_forecast_success(mocker):
    mock_open_meteo_service = mocker.patch("app.routers.weather.OpenMeteoService")
    mock_service_instance = mocker.MagicMock()
    mock_service_instance.get_weather_forecast.return_value = {
        "ubicacion": "Bogota",
        "latitud": 4.6097,
        "longitud": -74.0817,
        "pronostico_proximos_dias": [
            {
                "fecha": "2025-10-14",
                "temperatura_max": 20.0,
                "temperatura_min": 10.0,
                "probabilidad_precipitacion": 50,
            }
        ],
        "mensaje_info": "El clima para Bogotá, Colombia",
    }
    mock_open_meteo_service.return_value = mock_service_instance

    response = client.get("/api/v1/weather?latitude=4.6097&longitude=-74.0817&city=Bogota")

    assert response.status_code == 200
    assert response.json() == {
        "ubicacion": "Bogota",
        "latitud": 4.6097,
        "longitud": -74.0817,
        "temperatura_actual": None,
        "humedad_relativa": None,
        "pronostico_proximos_dias": [
            {
                "fecha": "2025-10-14",
                "temperatura_max": 20.0,
                "temperatura_min": 10.0,
                "probabilidad_precipitacion": 50,
            }
        ],
        "mensaje_info": "El clima para Bogotá, Colombia",
    }


def test_get_colombia_weather_forecast_missing_params():
    response = client.get("/api/v1/weather")
    assert response.status_code == 422
