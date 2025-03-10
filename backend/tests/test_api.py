import pytest
import httpx
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)

def test_get_tasks_unauthorized():
    response = client.get("/tasks")
    assert response.status_code == 403  # Should be forbidden without auth

def test_register_user():
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code in [200, 409]  # 409 if email already in use

def test_login():
    response = client.post("/login", json={
        "login_str": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code in [200, 401]  # 401 if invalid credentials

def test_create_task():
    # First, log in to get the token
    login_response = client.post("/login", json={
        "login_str": "test@example.com",
        "password": "testpass"
    })
    assert login_response.status_code == 200
    token = login_response.cookies.get("token")

    headers = {"Cookie": f"token={token}"}
    response = client.post("/tasks", json={"name": "New Task", "description": "Task description", "deadline":"2026-02-27T12:52:25"}, headers=headers)
    assert response.status_code == 200
    assert response.json()[0]["name"] == "New Task"

def test_get_task_not_found():
    response = client.get("/tasks/99999")
    assert response.status_code == 404
    assert response.json()["details"] == "Task doesn't found"

def test_logout():
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.json()["detail"] == "Logout successful"

def test_delete():
    # First, log in to get the token
    login_response = client.post("/login", json={
        "login_str": "test@example.com",
        "password": "testpass"
    })
    assert login_response.status_code == 200
    token = login_response.cookies.get("token")

    headers = {"Cookie": f"token={token}"}
    create_response = client.post("/tasks", json={"name": "New Task", "description": "Task description", "deadline":"2026-02-27T12:52:25"}, headers=headers)
    assert create_response.status_code == 200
    assert create_response.json()[0]["name"] == "New Task"
    
    response = client.delete(f"/tasks/{create_response.json()[0]['id']}")
    assert response.status_code == 200
