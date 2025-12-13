"""Tests for user profile endpoints."""
import pytest
from fastapi.testclient import TestClient


def create_user_and_login(client: TestClient, username="testuser", email="test@example.com"):
    """Helper function to create a user and get auth token."""
    client.post(
        "/api/auth/signup",
        json={
            "username": username,
            "email": email,
            "password": "testpassword123"
        }
    )
    
    response = client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": "testpassword123"
        }
    )
    
    return response.json()["access_token"]


def test_get_current_user_profile(client: TestClient):
    """Test getting current user's profile."""
    token = create_user_and_login(client)
    
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_profile_unauthorized(client: TestClient):
    """Test getting profile without authentication."""
    response = client.get("/api/users/me")
    assert response.status_code == 401


def test_update_user_profile(client: TestClient):
    """Test updating user profile."""
    token = create_user_and_login(client)
    
    response = client.put(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "Updated Name",
            "email": "updated@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["email"] == "updated@example.com"


def test_update_email_already_taken(client: TestClient):
    """Test updating email to one that's already taken."""
    # Create two users
    token1 = create_user_and_login(client, "user1", "user1@example.com")
    create_user_and_login(client, "user2", "user2@example.com")
    
    # Try to update user1's email to user2's email
    response = client.put(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token1}"},
        json={"email": "user2@example.com"}
    )
    assert response.status_code == 400
    assert "Email already in use" in response.json()["detail"]
