from fastapi.testclient import TestClient

from app.main import create_app


def test_read_root():
    app = create_app()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Open Weather Map API!"}
