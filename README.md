# Personal Finance Tracker API

Backend API for a personal finance tracker built with FastAPI and SQLAlchemy.

This repository is being used as a backend portfolio project focused on:

- REST API design
- database modeling and migrations
- user management
- password hashing
- test setup for CRUD logic

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker Compose
- Passlib with bcrypt
- Pytest

## Current Scope

Implemented today:

- user model and user CRUD flow
- duplicate email protection on create
- reusable 404 helper for missing users
- password hashing utility in `src/auth/hashing.py`
- tests for core CRUD behavior

In progress:

- login endpoint
- JWT authentication
- transactions, categories, budgets, and reports modules

## Project Structure

```text
personal_fin_tracker/
|-- alembic/
|-- src/
|   |-- auth/
|   |   |-- crud.py
|   |   |-- hashing.py
|   |   |-- models.py
|   |   |-- router.py
|   |   `-- schemas.py
|   |-- budget/
|   |-- categories/
|   |-- core/
|   |-- db/
|   |-- reports/
|   |-- transactions/
|   `-- main.py
|-- test/
|-- .env.example
|-- alembic.ini
|-- docker-compose.yml
`-- requirements.txt
```

## API Endpoints

### Users

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/users` | Create a user |
| `GET` | `/users/{user_id}` | Get user by id |
| `PUT` | `/users/{user_id}` | Update user |
| `DELETE` | `/users/{user_id}` | Delete user |

### Planned

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/login` | Authenticate user and return token |

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/personal_fin_tracker.git
cd personal_fin_tracker
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` from `.env.example` and set your PostgreSQL values.

### 5. Start PostgreSQL

```bash
docker-compose up -d
```

### 6. Run migrations

```bash
alembic upgrade head
```

### 7. Start the API

```powershell
$env:PYTHONPATH="src"
uvicorn src.main:app --reload
```

Docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Example Request

```bash
curl -X POST "http://127.0.0.1:8000/users" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"password\":\"secret123\"}"
```

## Notes

- `passlib` is installed in the project's `.venv`, so the IDE/interpreter should point there.
- Password hashing is already wired into user creation.
- Authentication and token handling are the next backend milestone.

## Roadmap

- add login endpoint
- issue and validate JWT tokens
- protect private routes
- implement transactions CRUD
- implement categories and budgets
- expand test coverage

## License

MIT
