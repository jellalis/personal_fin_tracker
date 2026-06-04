# 💰 Personal Finance Tracker API

A RESTful API built with Python and FastAPI for tracking personal finances. Built as a portfolio project to demonstrate core backend engineering skills: REST API design, PostgreSQL database management, SQLAlchemy ORM, JWT authentication, and Docker containerization.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Database | PostgreSQL |
| Infrastructure | Docker & Docker Compose |
| Authentication | JWT (python-jose) + passlib/bcrypt |
| Testing | pytest |
| DB Driver | psycopg2 |

---

## 📁 Project Structure

```
personal_fin_tracker/
├── src/
│   ├── main.py                   # FastAPI app entry point, router registration
│   ├── auth/                     # Authentication & user management (fully implemented)
│   │   ├── models.py             # User SQLAlchemy model
│   │   ├── schemas.py            # Pydantic schemas: UserBase, UserCreate, UserResponse, LoginRequest
│   │   ├── crud.py               # User CRUD operations + get_user_or_404 helper
│   │   ├── router.py             # User & auth endpoints
│   │   ├── hashing.py            # Password hashing: hash_pass(), ver_pass()
│   │   └── jwt.py                # JWT token creation & verification + oauth2_scheme
│   ├── transactions/             # Transactions module (fully implemented)
│   │   ├── models.py             # Transaction SQLAlchemy model (Enum type, timezone-aware created_at)
│   │   ├── schemas.py            # TransactionBase, TransactionCreate, TransactionResponse, TransactionType
│   │   ├── crud.py               # Transaction CRUD + get_transaction_or_404 helper (ownership enforced)
│   │   └── router.py             # Transaction endpoints (JWT protected)
│   ├── categories/               # Categories module (fully implemented)
│   │   ├── models.py             # Category model — user_id nullable (NULL = default category)
│   │   ├── schemas.py            # CategoryBase, CategoryCreate, CategoryResponse
│   │   ├── crud.py               # CRUD operations + get_categ_or_404 helper
│   │   └── router.py             # Category endpoints (JWT protected)
│   ├── budget/                   # Budget module (models only)
│   ├── reports/                  # Reports module (planned)
│   ├── core/
│   │   └── config.py             # App configuration via pydantic-settings
│   └── db/
│       └── database.py           # SQLAlchemy engine, SessionLocal, Base, get_db()
├── scripts/
│   └── seed_categories.py        # Seeds default categories into the database
├── test/
│   ├── conftest.py               # pytest fixtures (SQLite in-memory, full isolation per test)
│   └── test_crud.py              # Unit tests: create_user, get_user_not_found, delete_user
├── alembic/                      # Database migration files
├── docker-compose.yml
├── requirements.txt
├── .env                          # Secret keys — gitignored
└── .env.example
```

---

## 🗄️ Database Schema

```
users                           categories
├── id (PK)                     ├── id (PK)
├── name                        ├── name
├── email (unique)              └── user_id (FK → users, nullable)
├── hashed_password                  NULL = default (visible to all users)
└── enabled                          integer = custom (visible to owner only)

transactions                    budgets
├── id (PK)                     ├── id (PK)
├── amount                      ├── name
├── type (income/expense)       ├── amount
├── description (nullable)      ├── month
├── transaction_date            ├── user_id (FK → users)
├── created_at (timezone-aware) └── category_id (FK → categories)
├── user_id (FK → users)
└── category_id (FK → categories)
```

---

## 🔌 API Endpoints

### Auth
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | Login — returns JWT token | ❌ |

### Users
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/users` | Register new user | ❌ |
| GET | `/auth/users/{user_id}` | Get user by ID | ❌ |
| PUT | `/auth/users/{user_id}` | Update user | ❌ |
| DELETE | `/auth/users/{user_id}` | Delete user | ❌ |

### Categories
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/categories` | Create custom category | ✅ JWT |
| GET | `/categories` | Get all categories (defaults + own) | ✅ JWT |
| GET | `/categories/{category_id}` | Get category by ID | ✅ JWT |
| DELETE | `/categories/{category_id}` | Delete custom category | ✅ JWT |

### Transactions
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/transactions` | Create new transaction | ✅ JWT |
| GET | `/transactions` | Get all transactions for logged-in user | ✅ JWT |
| GET | `/transactions/{transaction_id}` | Get transaction by ID (ownership enforced) | ✅ JWT |
| DELETE | `/transactions/{transaction_id}` | Delete transaction (ownership enforced) | ✅ JWT |

### Budgets
> 🔲 Model exists — CRUD and routing pending

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone https://github.com/your-username/personal_fin_tracker.git
cd personal_fin_tracker
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:
```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=finance_tracker
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
SECRET_KEY=your-secret-key
```

### 5. Start the database

```bash
docker-compose up -d
```

### 6. Run database migrations

```bash
# Windows
$env:PYTHONPATH="src"; alembic upgrade head

# Mac/Linux
PYTHONPATH=src alembic upgrade head
```

### 7. Seed default categories

```bash
# Windows
$env:PYTHONPATH="src"; python scripts/seed_categories.py

# Mac/Linux
PYTHONPATH=src python scripts/seed_categories.py
```

### 8. Start the API server

```bash
# Windows
$env:PYTHONPATH="src"; uvicorn src.main:app --reload

# Mac/Linux
PYTHONPATH=src uvicorn src.main:app --reload
```

API: `http://127.0.0.1:8000`  
Swagger UI: `http://127.0.0.1:8000/docs`

---

### Run Tests

```bash
pytest
```

Tests use an SQLite in-memory database — no Docker needed to run the test suite.

---

## 🔒 Security Notes

- Passwords hashed with bcrypt via passlib — never stored as plain text
- Identical 401 responses for wrong password and unknown email — prevents email enumeration
- JWT tokens required for all category endpoints
- `.env` excluded from version control via `.gitignore`
- `bcrypt==4.0.1` pinned — passlib incompatible with bcrypt 5.x

---

## 📌 Current Status

| Feature | Status |
|---------|--------|
| Project structure & Docker | ✅ Complete |
| SQLAlchemy models (all 4 tables) | ✅ Complete |
| Alembic migrations | ✅ Complete |
| User CRUD + error handling | ✅ Complete |
| Password hashing | ✅ Complete |
| JWT infrastructure | ✅ Complete |
| POST /auth/login endpoint | ✅ Complete |
| pytest infrastructure + unit tests (3 passing) | ✅ Complete |
| Categories CRUD + routing + seeding | ✅ Complete |
| Code comments (all files documented) | ✅ Complete |
| Transactions CRUD + routing | ✅ Complete |
| Budgets CRUD + routing | 🔲 Pending |
| Ownership checks on category endpoints | 🔲 Pending |
| JWT protection on user endpoints | 🔲 Pending |
| Expanded test coverage (duplicate email, update, category, auth tests) | 🔲 Pending |

---

## 📄 License

MIT
