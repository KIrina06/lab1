import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_person():
    response = client.post("/api/v1/persons", json={"name": "Alice"})
    assert response.status_code == 201
    assert "Location" in response.headers

def test_get_all_persons():
    response = client.get("/api/v1/persons")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_person_not_found():
    response = client.get("/api/v1/persons/9999")
    assert response.status_code == 404
    assert "message" in response.json()

def test_validation_error():
    response = client.post("/api/v1/persons", json={})
    assert response.status_code == 400
    assert "errors" in response.json()
