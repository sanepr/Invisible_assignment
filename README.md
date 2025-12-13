# Expense Settlement Application

A full-stack application for managing split expenses between group members, consisting of a FastAPI backend and a React TypeScript frontend.

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

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **SQLite**: Default database (configurable to PostgreSQL, MySQL, etc.)
- **pytest**: Testing framework

### Frontend
- **React 19**: UI Framework
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Tailwind CSS**: Utility-first CSS framework
- **Vitest**: Unit testing
- **Cypress**: E2E testing

## Project Structure

```
.
├── app/                        # Backend (FastAPI)
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection and session
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── routes/                 # API routes
│   ├── utils/                  # Utility modules
│   └── tests/                  # Backend test suite
├── frontend/                   # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── api/               # API client library
│   │   ├── components/        # React components
│   │   ├── contexts/          # React contexts
│   │   ├── pages/             # Page components
│   │   ├── types/             # TypeScript type definitions
│   │   ├── test/              # Unit tests
│   │   ├── App.tsx            # Main App component
│   │   └── main.tsx           # Entry point
│   ├── cypress/               # E2E tests
│   ├── public/                # Static assets
│   ├── package.json           # Frontend dependencies
│   ├── vite.config.ts         # Vite configuration
│   └── README.md              # Frontend documentation
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- pip (Python package installer)
- npm or yarn

### Backend Setup

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

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API URL if needed (default: http://localhost:8000)
```

## Running the Application

### Start Backend

From the root directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API Base URL: `http://localhost:8000`
- Interactive API Docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API Docs (ReDoc): `http://localhost:8000/redoc`

### Start Frontend

From the frontend directory:

```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend URL: `http://localhost:5173`

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

### Backend Tests

Run all backend tests:

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

### Frontend Tests

Run unit tests:

```bash
cd frontend
npm test
```

Run E2E tests (requires both backend and frontend to be running):

```bash
cd frontend
npm run cypress
```

Run E2E tests in headless mode:

```bash
cd frontend
npm run cypress:headless
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
