import pytest
import requests
from fastapi import HTTPException

from app.models.weather import WeatherResponse
from app.services.open_meteo import OpenMeteoService


@pytest.fixture
def mock_open_meteo_response():
    """Fixture to provide a mock response from Open-Meteo API."""
    return {
        "latitude": 4.6097,
        "longitude": -74.0817,
        "hourly": {
            "time": [f"2025-10-14T{h:02d}:00" for h in range(24)],
            "temperature_2m": [15.0] * 24,
            "relative_humidity_2m": [80] * 24,
        },
        "daily": {
            "time": ["2025-10-14", "2025-10-15"],
            "temperature_2m_max": [20.0, 22.0],
            "temperature_2m_min": [10.0, 12.0],
            "precipitation_probability_max": [30, 40],
        },
    }


def test_prepare_response_success(mock_open_meteo_response, mocker):
    """
    Tests the successful mapping of API data to the WeatherResponse model.
    """
    service = OpenMeteoService(latitude=4.6097, longitude=-74.0817, city="Bogota")

    mock_datetime = mocker.patch("app.services.open_meteo.datetime")
    mock_datetime.utcnow.return_value.hour = 10

    response = service._prepare_response(mock_open_meteo_response)

    assert isinstance(response, WeatherResponse)
    assert response.ubicacion == "Bogota"
    assert response.latitud == 4.6097
    assert response.longitud == -74.0817
    assert response.temperatura_actual == 15.0
    assert response.humedad_relativa == 80
    assert len(response.pronostico_proximos_dias) == 2
    assert response.pronostico_proximos_dias[0].fecha == "2025-10-14"
    assert response.pronostico_proximos_dias[0].temperatura_max == 20.0


def test_get_weather_forecast_api_connection_error(mocker):
    """
    Tests the handling of a connection error when calling the Open-Meteo API.
    """
    service = OpenMeteoService(latitude=4.6097, longitude=-74.0817)

    mock_get = mocker.patch("app.services.open_meteo.requests.get")
    mock_get.side_effect = requests.exceptions.RequestException("Connection timed out")

    with pytest.raises(HTTPException) as exc_info:
        service.get_weather_forecast()

    assert exc_info.value.status_code == 500
    assert "Failed to connect to Open-Meteo API" in exc_info.value.detail


def test_get_weather_forecast_data_mapping_error(mock_open_meteo_response, mocker):
    """
    Tests the handling of a data mapping error (KeyError) when the API response is malformed.
    """
    del mock_open_meteo_response["hourly"]

    service = OpenMeteoService(latitude=4.6097, longitude=-74.0817)

    mock_get = mocker.patch("app.services.open_meteo.requests.get")
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_open_meteo_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with pytest.raises(HTTPException) as exc_info:
        service.get_weather_forecast()

    assert exc_info.value.status_code == 500
    assert "Error in data mapping" in exc_info.value.detail
