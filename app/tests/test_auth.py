"""Tests for authentication endpoints."""
import pytest
from fastapi.testclient import TestClient


def test_signup_success(client: TestClient):
    """Test successful user signup."""
    response = client.post(
        "/api/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data


def test_signup_duplicate_username(client: TestClient):
    """Test signup with duplicate username."""
    # Create first user
    client.post(
        "/api/auth/signup",
        json={
            "username": "testuser",
            "email": "test1@example.com",
            "password": "testpassword123"
        }
    )
    
    # Try to create another user with same username
    response = client.post(
        "/api/auth/signup",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


def test_signup_duplicate_email(client: TestClient):
    """Test signup with duplicate email."""
    # Create first user
    client.post(
        "/api/auth/signup",
        json={
            "username": "testuser1",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Try to create another user with same email
    response = client.post(
        "/api/auth/signup",
        json={
            "username": "testuser2",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client: TestClient):
    """Test successful login."""
    # Create user
    client.post(
        "/api/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/auth/login",
        json={
            "username": "nonexistent",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]
