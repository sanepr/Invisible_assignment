"""Tests for expense management endpoints."""
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


def create_group(client: TestClient, token: str, name="Test Group"):
    """Helper function to create a group."""
    response = client.post(
        "/api/groups",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": name}
    )
    return response.json()["id"]


def test_add_expense(client: TestClient):
    """Test adding an expense to a group."""
    token = create_user_and_login(client)
    group_id = create_group(client, token)
    
    response = client.post(
        "/api/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "group_id": group_id,
            "amount": 100.50,
            "description": "Dinner"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 100.50
    assert data["description"] == "Dinner"
    assert data["group_id"] == group_id


def test_add_expense_invalid_amount(client: TestClient):
    """Test adding expense with invalid amount."""
    token = create_user_and_login(client)
    group_id = create_group(client, token)
    
    response = client.post(
        "/api/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "group_id": group_id,
            "amount": -10,
            "description": "Invalid"
        }
    )
    assert response.status_code == 422  # Validation error


def test_get_group_expenses(client: TestClient):
    """Test getting all expenses for a group."""
    token = create_user_and_login(client)
    group_id = create_group(client, token)
    
    # Add two expenses
    client.post(
        "/api/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={"group_id": group_id, "amount": 50.0, "description": "Lunch"}
    )
    client.post(
        "/api/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={"group_id": group_id, "amount": 75.0, "description": "Dinner"}
    )
    
    # Get expenses
    response = client.get(
        f"/api/expenses/group/{group_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Verify both expenses are present (order may vary due to identical timestamps)
    amounts = {expense["amount"] for expense in data}
    assert amounts == {50.0, 75.0}


def test_get_group_balances(client: TestClient):
    """Test getting balance summary for a group."""
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
    
    token2 = client.post(
        "/api/auth/login",
        json={"username": "user2", "password": "testpassword123"}
    ).json()["access_token"]
    
    # Create group with user1
    group_id = create_group(client, token1)
    
    # Add user2 to group
    client.post(
        f"/api/groups/{group_id}/members",
        headers={"Authorization": f"Bearer {token1}"},
        json={"user_id": user2_id}
    )
    
    # User1 adds an expense of 100
    client.post(
        "/api/expenses",
        headers={"Authorization": f"Bearer {token1}"},
        json={"group_id": group_id, "amount": 100.0, "description": "Dinner"}
    )
    
    # Get balances
    response = client.get(
        f"/api/expenses/group/{group_id}/balances",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["group_id"] == group_id
    assert len(data["balances"]) == 2
    
    # User1 paid 100, should get back 50 (positive balance)
    # User2 paid 0, should pay 50 (negative balance)
    balances = {b["username"]: b["balance"] for b in data["balances"]}
    assert balances["user1"] == 50.0
    assert balances["user2"] == -50.0


def test_add_expense_not_member(client: TestClient):
    """Test adding expense to group user is not a member of."""
    token1 = create_user_and_login(client, "user1", "user1@example.com")
    token2 = create_user_and_login(client, "user2", "user2@example.com")
    
    # Create group with user1
    group_id = create_group(client, token1)
    
    # Try to add expense with user2
    response = client.post(
        "/api/expenses",
        headers={"Authorization": f"Bearer {token2}"},
        json={"group_id": group_id, "amount": 50.0, "description": "Test"}
    )
    assert response.status_code == 403
