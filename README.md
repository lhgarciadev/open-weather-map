# Open Weather Map API

This project provides a simple API to get the 7-day weather forecast for any location in Colombia.

## Installation and Setup

This project uses [uv](https://github.com/astral-sh/uv) as a package manager.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lhgarciadev/open-weather-map.git
    cd open-weather-map
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

## Running the Application

To run the application, use the following command:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://127.0.0.1:8000`.

## API Endpoint

### GET /weather

Fetches the 7-day weather forecast for a specific location in Colombia.

**Parameters:**

| Name      | Type    | Description                                     | Required | Example   |
| --------- | ------- | ----------------------------------------------- | -------- | --------- |
| `latitude`  | `float` | Geographic latitude of the location.            | Yes      | `4.6097`  |
| `longitude` | `float` | Geographic longitude of the location.           | Yes      | `-74.0817`|
| `city`      | `str`   | Optional name of the city for reference.        | No       | `Bogota`  |

**Example Request:**

```bash
curl "http://127.0.0.1:8000/weather?latitude=4.6097&longitude=-74.0817&city=Bogota"
```

**Example Response:**

```json
{
  "ubicacion": "Bogota",
  "latitud": 4.6097,
  "longitud": -74.0817,
  "temperatura_actual": 11.8,
  "humedad_relativa": 82,
  "pronostico_proximos_dias": [
    {
      "fecha": "2025-10-14",
      "temperatura_max": 18.8,
      "temperatura_min": 11.4,
      "probabilidad_precipitacion": 30
    },
    {
      "fecha": "2025-10-15",
      "temperatura_max": 17,
      "temperatura_min": 11.2,
      "probabilidad_precipitacion": 85
    },
    {
      "fecha": "2025-10-16",
      "temperatura_max": 17.6,
      "temperatura_min": 11.4,
      "probabilidad_precipitacion": 65
    },
    {
      "fecha": "2025-10-17",
      "temperatura_max": 17,
      "temperatura_min": 11.9,
      "probabilidad_precipitacion": 80
    },
    {
      "fecha": "2025-10-18",
      "temperatura_max": 17.9,
      "temperatura_min": 11.9,
      "probabilidad_precipitacion": 75
    },
    {
      "fecha": "2025-10-19",
      "temperatura_max": 18,
      "temperatura_min": 11.7,
      "probabilidad_precipitacion": 39
    },
    {
      "fecha": "2025-10-20",
      "temperatura_max": 17.1,
      "temperatura_min": 11.9,
      "probabilidad_precipitacion": 63
    }
  ],
  "mensaje_info": "7-day weather forecast for Bogota."
}
```
