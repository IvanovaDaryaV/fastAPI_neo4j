# тесты для приложения

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_person():
    response = client.post("/people", json={"name": "John", "age": "30"})
    assert response.status_code == 200
    assert response.json()["name"] == "John"
    assert response.json()["age"] == "30"

def test_get_all_people():
    response = client.get("/people")
    assert response.status_code == 200
    assert len(response.json()) > 0
