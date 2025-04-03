from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get():
    response = client.get("/users")  # ✅ To‘g‘ri URL
    assert response.status_code == 200

def test_post():
    data = {"full_name": "John Doe", "username": "john_doe", "email": "john.doe@example.com", "password": "secret123"}
    response = client.post("/users", json=data)  # ✅ To‘g‘ri URL
    assert response.status_code == 200

def test_put():
    data = {"full_name": "Jane Doe", "username": "jane_doe", "email": "jane.doe@example.com", "password": "secret123"}
    response = client.put("/users?user_id=1", json=data)  # ✅ To‘g‘ri URL
    assert response.status_code == 200

def test_delete():
    response = client.delete("/users?user_id=1")  # ✅ To‘g‘ri URL
    assert response.status_code == 200
