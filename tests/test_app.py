"""File to test API endpoints."""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello World!" in response.text
