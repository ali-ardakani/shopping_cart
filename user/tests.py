# tests.py
# This file contains the tests for user app.

from fastapi.testclient import TestClient
import time

def test_create_user(client: TestClient):
    response = client.post(
        "/user/register",
        json={
            "username": "test",
            "password": "test",
            "email": "test@email.com",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "message": "User test registered successfully"
    }
        
def test_login(client: TestClient):
    response = client.post(
        "/user/token",
        data={"username": "test", "password": "test"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
    
def test_logout(client: TestClient):
    token = client.post(
        "/user/token",
        data={"username": "test", "password": "test"},
    ).json()["access_token"]
    response = client.post(
        "/user/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Logged out successfully"
    }
    
def test_delete_user(client: TestClient):
    # Sleep for 1 second to avoid duplicate token error
    time.sleep(1)
    token = client.post(
        "/user/token",
        data={"username": "test", "password": "test"},
    ).json()["access_token"]
    response = client.delete(
        "/user/delete",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "User test deleted successfully"
    }
    