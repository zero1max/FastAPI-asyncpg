from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get():
    response = client.get("/api/users")
    assert response.status_code == 200

def test_post():
    data = {"full_name": "John Doe", "username": "john_doe", "email": "john.doe@example.com", "password": "secret123"}
    response = client.post("/api/users", json=data)
    assert response.status_code == 200

def test_put():
    data = {"full_name": "Jane Doe", "username": "jane_doe", "email": "jane.doe@example.com", "password": "secret123"}
    response = client.put("/api/users/1", json=data)
    assert response.status_code == 200

def test_delete():
    response = client.delete("/api/users/1")
    assert response.status_code == 200