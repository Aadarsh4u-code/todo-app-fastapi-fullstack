# Simple Todos App

## 1. Project Architecture Overview
```bash
app/
├── api/                         # Route handlers (HTTP endpoints)
│   └── v1/                      # API versioning
│       ├── users.py             # User management endpoints  
│       ├── router.py              # Login, Register, JWT routes
│       ├── todos.py             # Todo CRUD routes
│       └── ...
├── core/                        # Global config and security
│   ├── config.py                # Env-based settings for dev/staging/prod  
│   ├── security.py              # JWT, password hashing, RBAC
│   └── logging_config.py        # Production logging setup 
├── db/                          # Data access layer
│   ├── session.py               # Async DB sessions for Postgres & Mongo
│   ├── models/                  # SQLAlchemy models (Postgres)
│   │   ├── user.py              
│   │   └── todo.py
│   └── repository/              # Database CRUD operations
│       ├── user_repo.py
│       └── todo_repo.py
├── services/                    # Business logic layer
│   ├── user_service.py
│   ├── auth_service.py
│   └── todo_service.py
├── schemas/                     # Pydantic validation & I/O models
│   ├── user.py
│   ├── todo.py
│   └── router.py
├── tests/                       # Pytest unit/integration tests
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_todos.py
├── main.py                       # app entrypoint
└── alembic/                      # DB migrations
```

### Why this layout?
    It enforces Separation of Concerns, critical for maintainability and scalability:

  - API layer: HTTP endpoints, input/output handling only.
  - Service layer: Business logic (authorization checks, domain rules).
  - Repository layer: Data persistence — all DB operations.
  - Models/Schemas: Data validation and structure definitions.
  - Core: Global configurations (env, security, logging).
  - Tests: Automated verification for every feature.

## 2. Core Layer
  - core/config.py
    - Centralized configuration for all environments (dev, staging, prod).
    - Uses Pydantic BaseSettings to load environment variables.
    - Helps manage secrets, URLs, and database connections cleanly.

  - core/security.py
    - Handles JWT signing and verification.
    - Defines role-based access control (RBAC) using user roles (superadmin, admin, user).
    - Implements password hashing via bcrypt or passlib.

  - core/logging_config.py
    - Production logging setup (rotating logs, JSON format).
    - Essential for observability in deployments (e.g. on Render, Railway, or AWS).

## 3. Database Layer
 - db/session.py
    - Creates async SQLAlchemy AsyncSession for PostgreSQL.
    - Initializes MongoDB client (via motor) for hierarchical/non-relational data (e.g. charts, activity logs).
    - Dependency injection into repositories.
 - db/models/
   - SQLAlchemy models for relational data (Postgres).
   - Each model reflects a DB table (e.g. User, Todo).

   - db/repository/

     - Abstracts DB operations like:
       ```bash
       async def get_user_by_email(db, email: str): ...
       async def create_user(db, user: UserCreate): ...
       ```
     - Keeps services independent of DB technology.
     - Makes testing easier with mock repositories.

## 4. Schema Layer

  - Defines Pydantic models for request/response validation.
  - Example: UserCreate, UserRead, TodoCreate, TodoRead.
  - Shields the API from raw DB objects (prevents data leaks).



## 5. Service Layer

  - Encapsulates business logic.
  - Example in user_service.py:
    - Create user → check if exists → hash password → save → send welcome email.
  - Example in auth_service.py:
    - Validate credentials → issue JWT + refresh token → store refresh in Redis.
  - Keeps your endpoints clean and your rules centralized.

## 6. API Layer (Routers)

  - api/v1/ contains modular routers (e.g., auth.py, users.py, todos.py).
  - Each router imports relevant services and schemas.
  - Organized versioning (/api/v1) allows backward compatibility later.
    ```bash
    Example endpoint:
    
    @router.post("/login", response_model=Token)
    async def login_user(credentials: LoginSchema, db: Session = Depends(get_db)):
        return await auth_service.login(credentials, db)
    ```


## 7. Authentication & Authorization

  - JWT tokens (access + refresh).
  - Roles implemented as enums in the User model.
  - Decorator-based role checks:
      ```bash
      @role_required("admin")
      async def create_user(...):
          ...
      ```
  - Token blacklist (revocation) via Redis (optional but recommended).



## 8. Tests

  - Each module (auth, user, todo) has async pytest tests.
  - Use FastAPI’s TestClient for integration testing.
  - DB tests use transactional rollback to ensure isolation.
    ```bash
    Example:
    
    @pytest.mark.asyncio
    async def test_create_user(async_client):
        response = await async_client.post("/api/v1/users", json={"email": "test@x.com"})
        assert response.status_code == 201
    ```


## 9. Alembic Migrations

- Tracks changes in PostgreSQL models.
- Example migration auto-generated when you change a model:
  ```bash
    alembic revision --autogenerate -m "add is_active to user"
    alembic upgrade head
  ```
- Keeps DB schema version-controlled.



## 10. Environment Configuration

Three environments managed through .env files:
  - .env.dev — Local development
  - .env.staging — Pre-production testing
  - .env.prod — Production

Each sets DB URLs, log levels, secrets, and origins (CORS).



## 11. Docker & Deployment

- docker-compose.yml runs:
  - FastAPI app
  - PostgreSQL
  - MongoDB
  - Redis
- Simplifies onboarding and staging environments.
- CI/CD can reuse this config for automated tests.