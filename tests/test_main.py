"""Tests for FastAPI application."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}


def test_create_item():
    """Test item creation."""
    response = client.post("/items/1?name=Test&price=10.5&description=Test%20item")
    assert response.status_code == 200
    assert response.json()["message"] == "Item created"


def test_create_duplicate_item():
    """Test duplicate item creation."""
    client.post("/items/2?name=Test2&price=20.0")
    response = client.post("/items/2?name=Test2&price=20.0")
    assert response.status_code == 400
    assert response.json()["detail"] == "Item already exists"


def test_get_item():
    """Test getting an item."""
    client.post("/items/3?name=GetTest&price=30.0")
    response = client.get("/items/3")
    assert response.status_code == 200
    assert response.json()["name"] == "GetTest"


def test_get_nonexistent_item():
    """Test getting nonexistent item."""
    response = client.get("/items/999")
    assert response.status_code == 404


def test_update_item():
    """Test updating an item."""
    client.post("/items/4?name=Old&price=40.0")
    response = client.put("/items/4?name=New&price=45.0&description=Updated")
    assert response.status_code == 200


def test_delete_item():
    """Test deleting an item."""
    client.post("/items/5?name=DeleteMe&price=50.0")
    response = client.delete("/items/5")
    assert response.status_code == 200
