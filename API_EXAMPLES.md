# API Examples

This document provides practical examples of using the Expense Settlement API.

## Table of Contents
- [Authentication Flow](#authentication-flow)
- [User Management](#user-management)
- [Group Management](#group-management)
- [Expense Management](#expense-management)

## Authentication Flow

### 1. Sign Up

Create a new user account:

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "securepass123",
    "full_name": "Alice Smith"
  }'
```

Response:
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "full_name": "Alice Smith",
  "created_at": "2024-01-15T10:30:00"
}
```

### 2. Login

Authenticate and receive a JWT token:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "securepass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Important:** Save the `access_token` value. You'll need it for authenticated requests.

## User Management

### Get Current User Profile

```bash
TOKEN="your_access_token_here"

curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN"
```

Response:
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "full_name": "Alice Smith",
  "created_at": "2024-01-15T10:30:00"
}
```

### Update Profile

```bash
curl -X PUT http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Alice Johnson",
    "email": "alice.j@example.com"
  }'
```

## Group Management

### Create a Group

```bash
curl -X POST http://localhost:8000/api/groups \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weekend Trip",
    "description": "Expenses for our weekend getaway"
  }'
```

Response:
```json
{
  "id": 1,
  "name": "Weekend Trip",
  "description": "Expenses for our weekend getaway",
  "created_at": "2024-01-15T11:00:00"
}
```

### List My Groups

```bash
curl -X GET http://localhost:8000/api/groups \
  -H "Authorization: Bearer $TOKEN"
```

Response:
```json
[
  {
    "id": 1,
    "name": "Weekend Trip",
    "description": "Expenses for our weekend getaway",
    "created_at": "2024-01-15T11:00:00"
  }
]
```

### Get Group Details with Members

```bash
curl -X GET http://localhost:8000/api/groups/1 \
  -H "Authorization: Bearer $TOKEN"
```

Response:
```json
{
  "id": 1,
  "name": "Weekend Trip",
  "description": "Expenses for our weekend getaway",
  "created_at": "2024-01-15T11:00:00",
  "members": [
    {
      "user_id": 1,
      "username": "alice",
      "joined_at": "2024-01-15T11:00:00"
    },
    {
      "user_id": 2,
      "username": "bob",
      "joined_at": "2024-01-15T11:05:00"
    }
  ]
}
```

### Add User to Group

First, you need the user ID of the person you want to add. Then:

```bash
curl -X POST http://localhost:8000/api/groups/1/members \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2
  }'
```

Response:
```json
{
  "message": "User added to group successfully"
}
```

## Expense Management

### Add an Expense

```bash
curl -X POST http://localhost:8000/api/expenses \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "group_id": 1,
    "amount": 120.50,
    "description": "Hotel booking"
  }'
```

Response:
```json
{
  "id": 1,
  "group_id": 1,
  "paid_by_user_id": 1,
  "amount": 120.50,
  "description": "Hotel booking",
  "created_at": "2024-01-15T14:30:00"
}
```

### View Group Expense History

```bash
curl -X GET http://localhost:8000/api/expenses/group/1 \
  -H "Authorization: Bearer $TOKEN"
```

Response:
```json
[
  {
    "id": 1,
    "group_id": 1,
    "paid_by_user_id": 1,
    "amount": 120.50,
    "description": "Hotel booking",
    "created_at": "2024-01-15T14:30:00"
  },
  {
    "id": 2,
    "group_id": 1,
    "paid_by_user_id": 2,
    "amount": 85.00,
    "description": "Dinner",
    "created_at": "2024-01-15T19:00:00"
  }
]
```

### Get Balance Summary

This shows how much each group member owes or is owed (based on equal split):

```bash
curl -X GET http://localhost:8000/api/expenses/group/1/balances \
  -H "Authorization: Bearer $TOKEN"
```

Response:
```json
{
  "group_id": 1,
  "group_name": "Weekend Trip",
  "balances": [
    {
      "user_id": 1,
      "username": "alice",
      "balance": 17.75
    },
    {
      "user_id": 2,
      "username": "bob",
      "balance": -17.75
    }
  ]
}
```

**Interpretation:**
- Positive balance: User is owed money
- Negative balance: User owes money
- In this example: Alice paid $120.50 and Bob paid $85.00, total $205.50
- Equal split: $205.50 / 2 = $102.75 per person
- Alice: $120.50 - $102.75 = $17.75 (owed to Alice)
- Bob: $85.00 - $102.75 = -$17.75 (Bob owes)

## Complete Example Workflow

Here's a complete example of a typical workflow:

```bash
# 1. Sign up two users
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"pass123","full_name":"Alice"}'

curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","email":"bob@example.com","password":"pass123","full_name":"Bob"}'

# 2. Alice logs in
TOKEN_ALICE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"pass123"}' | jq -r '.access_token')

# 3. Alice creates a group
GROUP_ID=$(curl -s -X POST http://localhost:8000/api/groups \
  -H "Authorization: Bearer $TOKEN_ALICE" \
  -H "Content-Type: application/json" \
  -d '{"name":"Lunch Group","description":"Weekly lunch expenses"}' | jq -r '.id')

# 4. Alice adds Bob to the group (assuming Bob's ID is 2)
curl -X POST http://localhost:8000/api/groups/$GROUP_ID/members \
  -H "Authorization: Bearer $TOKEN_ALICE" \
  -H "Content-Type: application/json" \
  -d '{"user_id":2}'

# 5. Alice adds an expense
curl -X POST http://localhost:8000/api/expenses \
  -H "Authorization: Bearer $TOKEN_ALICE" \
  -H "Content-Type: application/json" \
  -d '{"group_id":'$GROUP_ID',"amount":50.00,"description":"Pizza lunch"}'

# 6. Bob logs in
TOKEN_BOB=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","password":"pass123"}' | jq -r '.access_token')

# 7. Bob adds an expense
curl -X POST http://localhost:8000/api/expenses \
  -H "Authorization: Bearer $TOKEN_BOB" \
  -H "Content-Type: application/json" \
  -d '{"group_id":'$GROUP_ID',"amount":30.00,"description":"Coffee"}'

# 8. Check the balance summary
curl -X GET http://localhost:8000/api/expenses/group/$GROUP_ID/balances \
  -H "Authorization: Bearer $TOKEN_ALICE"
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Browse all available endpoints
- See request/response schemas
- Try out API calls directly from your browser
- Authenticate using the "Authorize" button
