import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_person():
    response = client.post("/persons", json={"name": "Alice"})
    assert response.status_code == 201
    assert "Location" in response.headers

def test_get_all_persons():
    response = client.get("/persons")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_person_not_found():
    response = client.get("/persons/9999")
    assert response.status_code == 404
    assert "message" in response.json()

def test_validation_error():
    response = client.post("/persons", json={})
    assert response.status_code == 400
    assert "errors" in response.json()