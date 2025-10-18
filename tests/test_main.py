from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


def test_read_root():
    app = create_app()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Open Weather Map API!"}


def test_docs_disabled_in_production(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")

    # Clear the settings cache to reload the environment variable
    get_settings.cache_clear()

    app = create_app()
    client = TestClient(app)

    response = client.get("/docs")
    assert response.status_code == 404

    response = client.get("/redoc")
    assert response.status_code == 404

    response = client.get("/openapi.json")
    assert response.status_code == 404

    # Clean up environment variable and cache for other tests
    monkeypatch.delenv("ENVIRONMENT")
    get_settings.cache_clear()
