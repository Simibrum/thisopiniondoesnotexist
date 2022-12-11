"""File to test API endpoints."""
from httpx import AsyncClient

from fastapi.testclient import TestClient
import pytest
from app import app
from app.models.data_models import Post

client = TestClient(app)


# ------------------------------------------------------------------------------
# Test the endpoints
def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "This is a test" in response.text


@pytest.mark.anyio
async def test_upload_post(client: AsyncClient):
    """Test posting post data to the database."""
    post_data = {
        "day": 1,
        "month": 2,
        "year": 2022,
        "title": "February Test",
        "content": "Test February Content"
    }
    response = await client.post("/posts", json=post_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "February Test"
    assert "id" in data
    post_id = data["id"]
    post_obj = await Post.get(id=post_id)
    assert post_obj.id == post_id
