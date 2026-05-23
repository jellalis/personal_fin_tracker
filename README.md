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
│   ├── transactions/             # Transactions module (models only)
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
├── tests/
│   ├── conftest.py               # pytest fixtures
│   └── test_crud.py              # Unit tests
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
└── hashed_password                  NULL = default (visible to all users)
                                     integer = custom (visible to owner only)

transactions                    budgets
├── id (PK)                     ├── id (PK)
├── amount                      ├── amount
├── description                 ├── month
├── date                        ├── user_id (FK → users)
├── user_id (FK → users)        └── category_id (FK → categories)
└── category_id (FK → categories)
```

---

## 🔌 API Endpoints

### Auth
| Method | Endpoint | Description | Auth | Status |
|--------|----------|-------------|------|--------|
| POST | `/auth/login` | Login, returns JWT token | ❌ | ✅ |

### Users
| Method | Endpoint | Description | Auth | Status |
|--------|----------|-------------|------|--------|
| POST | `/users` | Register new user | ❌ | ✅ |
| GET | `/users/{user_id}` | Get user by ID | ❌ | ✅ |
| PUT | `/users/{user_id}` | Update user | ❌ | ✅ |
| DELETE | `/users/{user_id}` | Delete user | ❌ | ✅ |

### Categories
| Method | Endpoint | Description | Auth | Status |
|--------|----------|-------------|------|--------|
| POST | `/categories` | Create custom category | ✅ | ✅ |
| GET | `/categories` | Get all categories (defaults + own) | ✅ | ✅ |
| GET | `/categories/{category_id}` | Get category by ID | ✅ | ✅ |
| DELETE | `/categories/{category_id}` | Delete custom category | ✅ | ✅ |

### Transactions / Budgets
> 🔲 Models exist — CRUD and routing pending

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
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
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

---

## 🔒 Security Notes

- Passwords hashed with bcrypt via passlib (never stored as plain text)
- Identical 401 responses for wrong password and user not found — prevents email enumeration
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
| pytest infrastructure + first test | ✅ Complete |
| Categories CRUD + routing + seeding | ✅ Complete |
| Transactions CRUD + routing | 🔲 Pending |
| Budgets CRUD + routing | 🔲 Pending |
| Protected routes (auth middleware) | 🔲 Pending |
| Expanded test coverage | 🔲 Pending |

---

## 📄 License

MIT