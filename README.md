# Expense Settlement API

A FastAPI-based REST API for managing split expenses between group members with JWT authentication.

## Features

- **User Management**
  - User sign-up with email validation
  - JWT-based authentication
  - User profile management (view and update)

- **Group Management**
  - Create expense groups
  - Add members to groups
  - View group details with member list

- **Expense Management**
  - Add expenses to groups
  - View expense history
  - Calculate balance summaries (equal split)
  - Track who paid and who owes

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **SQLite**: Default database (configurable to PostgreSQL, MySQL, etc.)
- **pytest**: Testing framework

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection and session
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   ├── group.py           # Group and UserGroup models
│   │   └── expense.py         # Expense model
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py            # User schemas
│   │   ├── group.py           # Group schemas
│   │   └── expense.py         # Expense schemas
│   ├── routes/                 # API routes
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User profile endpoints
│   │   ├── groups.py          # Group management endpoints
│   │   └── expenses.py        # Expense management endpoints
│   ├── utils/                  # Utility modules
│   │   ├── __init__.py
│   │   └── auth.py            # Authentication utilities
│   └── tests/                  # Test suite
│       ├── __init__.py
│       ├── conftest.py        # Test configuration
│       ├── test_auth.py       # Auth endpoint tests
│       ├── test_users.py      # User endpoint tests
│       ├── test_groups.py     # Group endpoint tests
│       └── test_expenses.py   # Expense endpoint tests
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Invisible_assignment
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. The database will be automatically created when you first run the application.

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API Base URL: `http://localhost:8000`
- Interactive API Docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API Docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### User Profile

- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user profile

### Groups

- `POST /api/groups` - Create a new group
- `GET /api/groups` - List user's groups
- `GET /api/groups/{group_id}` - Get group details with members
- `POST /api/groups/{group_id}/members` - Add user to group

### Expenses

- `POST /api/expenses` - Add expense to group
- `GET /api/expenses/group/{group_id}` - Get group expense history
- `GET /api/expenses/group/{group_id}/balances` - Get balance summary

## API Usage Examples

### 1. Register a new user

```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "full_name": "John Doe"
  }'
```

### 2. Login and get token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
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

### 3. Create a group (requires authentication)

```bash
curl -X POST "http://localhost:8000/api/groups" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weekend Trip",
    "description": "Expenses for our weekend getaway"
  }'
```

### 4. Add an expense

```bash
curl -X POST "http://localhost:8000/api/expenses" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "group_id": 1,
    "amount": 150.50,
    "description": "Hotel booking"
  }'
```

### 5. Get balance summary

```bash
curl -X GET "http://localhost:8000/api/expenses/group/1/balances" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Running Tests

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest app/tests/test_auth.py
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

## Configuration

The application can be configured using environment variables in the `.env` file:

- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: Secret key for JWT token generation
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `APP_NAME`: Application name
- `DEBUG`: Debug mode (default: True)

## Database Migration

For production use, consider using Alembic for database migrations:

```bash
# Initialize Alembic
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use a production-grade database (PostgreSQL, MySQL)
3. Set a strong `SECRET_KEY`
4. Configure proper CORS origins in `app/main.py`
5. Use a production ASGI server like Gunicorn with Uvicorn workers:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens are used for stateless authentication
- All authenticated endpoints require valid JWT tokens
- Users can only access groups they are members of
- Input validation is enforced using Pydantic schemas

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## License

This project is provided as-is for educational and commercial purposes.
