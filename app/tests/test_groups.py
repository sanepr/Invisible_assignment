"""Tests for group management endpoints."""
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


def test_create_group(client: TestClient):
    """Test creating a new group."""
    token = create_user_and_login(client)
    
    response = client.post(
        "/api/groups",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Group",
            "description": "A test group"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Group"
    assert data["description"] == "A test group"
    assert "id" in data


def test_list_user_groups(client: TestClient):
    """Test listing user's groups."""
    token = create_user_and_login(client)
    
    # Create a group
    client.post(
        "/api/groups",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Group"}
    )
    
    # List groups
    response = client.get(
        "/api/groups",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Group"


def test_get_group_details(client: TestClient):
    """Test getting group details with members."""
    token = create_user_and_login(client)
    
    # Create a group
    create_response = client.post(
        "/api/groups",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Group"}
    )
    group_id = create_response.json()["id"]
    
    # Get group details
    response = client.get(
        f"/api/groups/{group_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Group"
    assert "members" in data
    assert len(data["members"]) == 1
    assert data["members"][0]["username"] == "testuser"


def test_add_user_to_group(client: TestClient):
    """Test adding a user to a group."""
    # Create two users
    token1 = create_user_and_login(client, "user1", "user1@example.com")
    
    user2_response = client.post(
        "/api/auth/signup",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "testpassword123"
        }
    )
    user2_id = user2_response.json()["id"]
    
    # Create a group with user1
    create_response = client.post(
        "/api/groups",
        headers={"Authorization": f"Bearer {token1}"},
        json={"name": "Test Group"}
    )
    group_id = create_response.json()["id"]
    
    # Add user2 to the group
    response = client.post(
        f"/api/groups/{group_id}/members",
        headers={"Authorization": f"Bearer {token1}"},
        json={"user_id": user2_id}
    )
    assert response.status_code == 201
    assert "message" in response.json()


def test_add_user_to_nonexistent_group(client: TestClient):
    """Test adding user to non-existent group."""
    token = create_user_and_login(client)
    
    response = client.post(
        "/api/groups/999/members",
        headers={"Authorization": f"Bearer {token}"},
        json={"user_id": 1}
    )
    assert response.status_code == 404


def test_access_group_not_member(client: TestClient):
    """Test accessing a group the user is not a member of."""
    # Create two users
    token1 = create_user_and_login(client, "user1", "user1@example.com")
    token2 = create_user_and_login(client, "user2", "user2@example.com")
    
    # Create a group with user1
    create_response = client.post(
        "/api/groups",
        headers={"Authorization": f"Bearer {token1}"},
        json={"name": "Test Group"}
    )
    group_id = create_response.json()["id"]
    
    # Try to access with user2
    response = client.get(
        f"/api/groups/{group_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 403
