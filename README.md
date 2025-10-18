[![Python application test with GitHub Actions](https://github.com/lhgarciadev/open-weather-map/actions/workflows/testing-ci.yml/badge.svg?event=pull_request)](https://github.com/lhgarciadev/open-weather-map/actions/workflows/testing-ci.yml)

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
    make install
    ```

## Project Structure

This project is structured following the best practices recommended by FastAPI for building larger, scalable applications. This modular approach helps in separating concerns and makes the codebase easier to maintain and extend.

```
open-weather-map/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Creates and initializes the FastAPI application
│   │
│   ├── models/                    # Pydantic models (schemas)
│   │   ├── __init__.py
│   │   └── weather.py             # WeatherRequest and WeatherResponse models
│   │
│   ├── routers/                   # Routes grouped by functionality
│   │   ├── __init__.py
│   │   └── weather.py             # Endpoint /weather/forecast
│   │
│   ├── services/                  # Business logic or external integration
│   │   ├── __init__.py
│   │   └── open_meteo.py          # HTTP client for Open-Meteo API
│   │
│   └── core/                      # Infrastructure and core utilities
│       ├── __init__.py
│       ├── config.py              # Application settings and environment variables
│       ├── exceptions.py          # Centralized exception handling
│       └── logging_config.py      # Application-wide logging configuration
│
├── tests/
│   ├── routers/
│   │   └── test_weather.py        # Tests FastAPI endpoint
│   ├── services/
│   │   └── test_open_meteo.py     # Tests external API integration
│   └── test_main.py               # Smoke test for the app
```

### Component Breakdown

*   **`app/main.py`**: The main entry point that initializes the FastAPI application and includes all the necessary components like routers and exception handlers.
*   **`app/core/`**: Contains all the cross-cutting concerns and core infrastructure.
    *   `config.py`: Manages application settings and environment variables.
    *   `exceptions.py`: Defines custom application-specific exceptions.
    *   `logging_config.py`: Configures logging for the entire application.
*   **`app/models/`**: Defines the Pydantic models that determine the data shape (schema) for API requests and responses.
*   **`app/routers/`**: Contains the API endpoints. Each file groups related routes, which are then included in the main application.
*   **`app/services/`**: Holds the business logic. In this case, it contains the logic for interacting with the external Open-Meteo API.
*   **`tests/`**: Contains all the tests, mirroring the application's structure to ensure code quality and correctness.

## Running the Application

This project uses a `Makefile` to simplify common tasks.

### Local Development

To run the application in development mode (with hot-reloading and API docs):

```bash
make run-dev
```

### Local Production

To run the application in production mode (no hot-reloading, no API docs):

```bash
make run-pro
```

The application will be available at `http://127.0.0.1:8000`.

## Running with Docker

### Build the Image

First, build the Docker image using the provided `Makefile` command:

```bash
make docker-build
```

### Run in Production Mode

To run the container in production mode (recommended for deployment):

```bash
make docker-run-pro
```

### Run in Development Mode

To run the container in development mode, which mounts the local `app` directory for hot-reloading:

```bash
make docker-run-dev
```

## API Endpoint

### GET /api/v1/weather

Fetches the 7-day weather forecast for a specific location in Colombia.

**Parameters:**

| Name      | Type    | Description                                     | Required | Example   |
| --------- | ------- | ----------------------------------------------- | -------- | --------- |
| `latitude`  | `float` | Geographic latitude of the location.            | Yes      | `4.6097`  |
| `longitude` | `float` | Geographic longitude of the location.           | Yes      | `-74.0817`|
| `city`      | `str`   | Optional name of the city for reference.        | No       | `Bogota`  |

**Example Request:**

```bash
curl "http://127.0.0.1:8000/api/v1/weather?latitude=4.6097&longitude=-74.0817&city=Bogota"
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
    }
  ],
  "mensaje_info": "7-day weather forecast for Bogota."
}
```
