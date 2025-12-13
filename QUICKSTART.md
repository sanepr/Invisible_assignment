# Quick Start Guide

This guide will help you quickly set up and run the Expense Settlement Application (both backend and frontend).

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

## Setup & Run in 5 Minutes

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Invisible_assignment
```

### 2. Set Up Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file (optional - uses defaults if not created)
cp .env.example .env

# Start the backend server
uvicorn app.main:app --reload
```

The backend API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 3. Set Up Frontend (in a new terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file (optional - uses defaults)
cp .env.example .env

# Start the development server
npm run dev
```

The frontend will be available at:
- **Frontend**: http://localhost:5173

## Quick Test

### Using the Web Interface

1. Open http://localhost:5173 in your browser
2. Click "Get Started" to create an account
3. Fill out the signup form and submit
4. Login with your credentials
5. Create a new group
6. Add expenses and see the balance summary

### Using the API (with curl)

```bash
# 1. Sign up
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'

# Save the token from the response

# 3. Get your profile
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. Create a group
curl -X POST http://localhost:8000/api/groups \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Group",
    "description": "My first group"
  }'
```

## Running Tests

### Backend Tests

```bash
# From the root directory
pytest

# With coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
# From the frontend directory
cd frontend

# Run unit tests
npm test

# Run E2E tests (requires Cypress installation and both servers running)
npm install --save-dev cypress  # First time only
npm run cypress
```

## Project Structure Overview

```
Invisible_assignment/
├── app/                    # Backend (FastAPI)
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   ├── schemas/           # Pydantic schemas
│   └── tests/             # Backend tests
├── frontend/              # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── api/          # API client library
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── test/         # Frontend tests
│   └── cypress/          # E2E tests
└── requirements.txt      # Python dependencies
```

## Key Features Implemented

### Backend
- ✅ User authentication (JWT)
- ✅ Group management
- ✅ Expense tracking
- ✅ Balance calculations
- ✅ RESTful API
- ✅ Unit tests with pytest

### Frontend
- ✅ React + TypeScript
- ✅ Authentication flow (login/signup)
- ✅ Dashboard with group overview
- ✅ Create and manage groups
- ✅ Add and view expenses
- ✅ Balance summary display
- ✅ Responsive design with Tailwind CSS
- ✅ API client library
- ✅ Unit tests with Vitest
- ✅ E2E tests with Cypress

## Common Issues & Solutions

### Backend Issues

**Issue**: Module not found errors
```bash
# Solution: Make sure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Issue**: Database errors
```bash
# Solution: Delete the database file and restart
rm *.db
uvicorn app.main:app --reload
```

### Frontend Issues

**Issue**: `npm install` fails with Cypress
```bash
# Solution: Cypress requires separate installation
npm install
# Skip Cypress for now, install it later when needed:
npm install --save-dev cypress
```

**Issue**: API connection errors
```bash
# Solution: Make sure backend is running on http://localhost:8000
# Or update VITE_API_URL in frontend/.env
```

**Issue**: Build errors
```bash
# Solution: Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs for interactive API documentation
2. **Customize**: Modify the code to add your own features
3. **Deploy**: See the main README for production deployment instructions
4. **Contribute**: Check the contributing guidelines and submit a PR

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- See [API_EXAMPLES.md](API_EXAMPLES.md) for more API usage examples
- Review the [frontend/README.md](frontend/README.md) for frontend-specific documentation

## Architecture Overview

```
┌─────────────┐      HTTP/REST      ┌─────────────┐
│   Browser   │ ◄──────────────────► │   React     │
│             │   (Axios Client)     │  Frontend   │
└─────────────┘                      └─────────────┘
                                            │
                                            │ API Calls
                                            ▼
                                     ┌─────────────┐
                                     │   FastAPI   │
                                     │   Backend   │
                                     └─────────────┘
                                            │
                                            │ SQLAlchemy
                                            ▼
                                     ┌─────────────┐
                                     │   SQLite    │
                                     │  Database   │
                                     └─────────────┘
```

### Data Flow

1. User interacts with React frontend
2. Frontend calls API client methods
3. API client sends authenticated HTTP requests to backend
4. Backend validates JWT token and processes request
5. Backend queries/updates database via SQLAlchemy ORM
6. Backend returns JSON response
7. Frontend updates UI with response data

## License

This project is provided as-is for educational and commercial purposes.
