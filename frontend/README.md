# Expense Splitter Frontend

A modern TypeScript React application for managing shared expenses with groups. Built with React, TypeScript, Tailwind CSS, and Vite.

## Features

- **Authentication**: JWT-based login and signup with token management
- **Group Management**: Create and manage expense groups
- **Expense Tracking**: Add expenses and view detailed history
- **Balance Summary**: Automatic calculation of who owes what
- **Responsive Design**: Mobile-friendly UI with Tailwind CSS
- **Type Safety**: Full TypeScript support
- **API Client Library**: Reusable API client with authentication handling

## Tech Stack

- **React 19** - UI Framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Vitest** - Unit testing
- **Cypress** - E2E testing
- **Testing Library** - Component testing utilities

## Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on `http://localhost:8000` (or configured via environment variable)

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Configure the API URL in `.env` if needed:
```
VITE_API_URL=http://localhost:8000
```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Building for Production

Build the application:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Testing

### Unit Tests

Run unit tests with Vitest:
```bash
npm test
```

Run tests in watch mode:
```bash
npm test -- --watch
```

Run tests with UI:
```bash
npm run test:ui
```

Run tests with coverage:
```bash
npm run test:coverage
```

### E2E Tests

Run Cypress tests interactively:
```bash
npm run cypress
```

Run Cypress tests in headless mode:
```bash
npm run cypress:headless
```

**Note**: Make sure both the backend API and frontend dev server are running before executing E2E tests.

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API client and services
│   │   ├── client.ts     # Axios client with interceptors
│   │   └── services.ts   # API service methods
│   ├── components/       # Reusable components
│   │   ├── Layout.tsx    # Main layout with navigation
│   │   └── ProtectedRoute.tsx  # Route wrapper for auth
│   ├── contexts/         # React contexts
│   │   └── AuthContext.tsx     # Authentication context
│   ├── pages/            # Page components
│   │   ├── HomePage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── SignupPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── GroupsPage.tsx
│   │   ├── GroupDetailPage.tsx
│   │   └── ProfilePage.tsx
│   ├── types/            # TypeScript type definitions
│   │   └── index.ts
│   ├── test/             # Test files and setup
│   │   ├── setup.ts
│   │   ├── LoginPage.test.tsx
│   │   └── apiClient.test.ts
│   ├── App.tsx           # Main App component with routing
│   ├── main.tsx          # Application entry point
│   └── index.css         # Global styles
├── cypress/              # Cypress E2E tests
│   ├── e2e/
│   │   ├── auth.cy.ts
│   │   └── navigation.cy.ts
│   └── support/
│       ├── commands.ts
│       └── e2e.ts
├── public/               # Static assets
├── index.html            # HTML template
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Dependencies and scripts
```

## API Client Library

The application includes a well-structured API client library:

### Authentication
```typescript
import { authService } from './api/services';

// Login
const { access_token } = await authService.login({ 
  username: 'user', 
  password: 'pass' 
});

// Signup
const user = await authService.signup({
  username: 'newuser',
  email: 'user@example.com',
  password: 'password',
  full_name: 'New User'
});

// Logout
authService.logout();
```

### Groups
```typescript
import { groupService } from './api/services';

// Create group
const group = await groupService.createGroup({
  name: 'Trip to Paris',
  description: 'Weekend trip expenses'
});

// Get groups
const groups = await groupService.getGroups();

// Get group details
const groupDetails = await groupService.getGroup(groupId);
```

### Expenses
```typescript
import { expenseService } from './api/services';

// Add expense
const expense = await expenseService.createExpense({
  group_id: 1,
  amount: 50.00,
  description: 'Dinner'
});

// Get balances
const balances = await expenseService.getBalances(groupId);
```

## Authentication Flow

1. User signs up or logs in
2. JWT token is stored in localStorage
3. Token is automatically included in all API requests via Axios interceptor
4. Protected routes check authentication status
5. Invalid/expired tokens trigger automatic logout and redirect to login

## Available Pages

- `/` - Landing page with feature overview
- `/login` - User login
- `/signup` - User registration
- `/dashboard` - User dashboard with group list
- `/groups/new` - Create new group
- `/groups/:id` - Group details with expenses and balances
- `/profile` - User profile management

## Environment Variables

- `VITE_API_URL` - Backend API base URL (default: `http://localhost:8000`)

## Styling

The application uses Tailwind CSS for styling with a clean, modern design:

- Responsive layouts for mobile and desktop
- Consistent color scheme with blue accent color
- Loading states and error handling
- Form validation and user feedback

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Run linting and tests
5. Submit a pull request

## License

This project is provided as-is for educational and commercial purposes.
