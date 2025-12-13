# AI_USAGE_JOURNAL

## Purpose

This document describes how AI tools were used during the assessment, architectural ownership, and human accountability.
---

## 1. AI Tool Identification

**Primary AI Assistant:** GitHub Copilot (Workspace Agent)  
**Model Class:** GPT-4–level model with code and architecture understanding  
**Interface:** GitHub Copilot Workspace (repository-aware)

**Capabilities Utilized:**
- Code generation and refactoring
- Debugging assistance
- Architecture ideation and comparison
- Documentation drafting
---

## 2. Tools, Technologies, and Stack

### AI Tools
- **GitHub Copilot Workspace**
  - Primary AI tool used throughout development
  - Leveraged for scaffolding, pattern recall, and rapid iteration
  - Integrated with repository context and git history

### Technologies Implemented
- **Frontend:** React 19, TypeScript (strict mode), Vite, Tailwind CSS v4
- **Backend Integration:** Existing FastAPI (Python) backend
- **Testing:** Vitest (unit tests), Cypress (E2E testing)
- **Infrastructure:** Terraform, AWS services
- **Version Control:** Git with structured, traceable commits

---

## 3. Development Process & AI Involvement

### 3.1 Architecture & Initial Planning

**Representative Prompts:**
- Generate a scalable FastAPI project structure for group expense splitting
- Suggest a relational schema for users, groups, memberships, and expenses
- How should secrets be managed in a Terraform-based cloud deployment?

**AI Contributions:**
- Generated baseline project structures and module boundaries
- Proposed initial REST API surface area
- Drafted an early ER diagram concept
- Generated Terraform examples for database and secrets management

**Manual Fixes:**
- Simplified over-engineered abstractions suggested by AI
- Formalized schemas and diagrams manually
- Adjusted IAM, networking, and secrets handling to fit real-world cloud constraints
- Made explicit tradeoffs to optimize for maintainability over theoretical purity

---

### 3.2 Code Implementation

**Representative Prompts:**
- Generate a FastAPI signup endpoint with Pydantic and SQLAlchemy
- Implement JWT authentication following standard security practices
- Create a type-safe TypeScript API client for a FastAPI backend

**AI Contributions:**
- Generated boilerplate for routes, schemas, and ORM models
- Drafted JWT authentication flows
- Created initial TypeScript client stubs and DTOs

**Manual Fixes:**
- Enforced domain invariants (e.g., group membership validation)
- Corrected schema/ORM mismatches
- Standardized error semantics and HTTP status codes
- Ensured client types aligned with backend OpenAPI contracts

---

### 3.3 Code Quality & Testing

**Representative Prompts:**
- Write pytest tests for FastAPI authentication and expense endpoints
- Suggest fixtures for SQLAlchemy and FastAPI test isolation
- How can authentication be mocked in tests?

**AI Contributions:**
- Generated baseline fixtures and happy-path tests
- Suggested authentication mocking strategies

**Manual Fixes:**
- Added negative, boundary, and security-focused test cases
- Updated outdated library usage
- Enforced linting, formatting, and CI compatibility
- Defined what constituted “meaningful coverage” beyond basic success paths

---

### 3.4 Documentation & Observability

**Representative Prompts:**
- Outline a comprehensive README for onboarding
- Suggest observability instrumentation for FastAPI
- Draft security considerations for a sensitive backend

**AI Contributions:**
- Drafted initial onboarding documentation
- Generated observability examples
- Proposed security best-practice sections

**Manual Fixes:**
- Edited documentation for precision and correctness
- Added threat modeling and compliance-oriented language
- Ensured documentation reflected operational reality, not theoretical setups

---

## 4. Frontend Development

### Frontend Architecture & State Management
- React Context used for authentication state
- API client isolated behind a typed service layer
- Protected routing implemented with explicit loading and failure states

**AI Role:** Generated scaffolding and examples  
**Human Role:** Ensured correctness across navigation and lifecycle edge cases

---

### UI Components & Layout
- Dashboard, group management, expense tracking, and profile pages
- Mobile-first responsive design using Tailwind CSS

**Manual Fixes:**
- Diagnosed and resolved layout and background conflicts
- Verified rendering across breakpoints and navigation states

---

## 5. Debugging & Production Readiness

### Dependency & Runtime Issues
- Diagnosed bcrypt C-extension loading failures
- Addressed bcrypt 72-byte password constraint

**Outcome:**
- Multi-layer validation implemented (schema, runtime, frontend)
- Errors converted from runtime failures to user-safe HTTP responses

---

## 6. Infrastructure as Code (IaC)

**AI Contributions:**
- Terraform module scaffolding
- Environment separation (dev/prod)
- Secrets management and observability templates
- CI/CD pipeline examples

**Manual Fixes:**
- Replaced placeholders with organization-appropriate values
- Ensured secrets were never committed
- Documented handoff points for platform and DevOps teams

---

## 7. Manual Interventions & Human Accountability

The following tasks required explicit human action and validation:
- Dependency installation and environment setup
- Backend server restarts
- Cloud and Terraform customization
- Secrets provisioning
- CI/CD activation

These actions reinforce that **production accountability remained human-owned**.

---

## 8. Code Quality & Security Outcomes

- Successful frontend build
- TypeScript strict mode enabled with zero errors
- Unit tests passing (9/9)
- E2E testing framework configured
- Input validation enforced at multiple layers
- JWT security best practices applied

---

## 9. AI Effectiveness Assessment

### Strengths
- Rapid scaffolding and boilerplate generation
- Strong recall of common architectural patterns
- Effective debugging assistance
- High-quality documentation drafts

### Limitations
- No runtime or organizational context
- Limited edge-case reasoning
- Requires senior review for correctness and security

---