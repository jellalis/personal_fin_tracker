# 💰 Personal Finance Tracker API

Most people don't know where their money goes. Spreadsheets are cumbersome, and
off-the-shelf apps lock your data behind subscriptions with no programmatic access.

This is a production-ready REST API for personal finance management — track income
and expenses, organise them into categories, and own your data completely.
Built with FastAPI and PostgreSQL, with JWT authentication, full test coverage, and CI/CD.

> 🔗 **Live API:** https://personal-fin-tracker-elq3.onrender.com
> 📖 **Interactive Docs (Swagger):** https://personal-fin-tracker-elq3.onrender.com/docs

---

## ✨ Features

- **JWT Authentication** — secure register/login flow with bcrypt password hashing
- **Transaction Tracking** — log income and expenses with type, amount, date, and category
- **Category Management** — system-wide default categories + personal custom ones per user
- **Ownership Enforcement** — users can only access their own data (IDOR protection)
- **Dockerised** — runs locally with a single `docker-compose up`

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
│   ├── auth/                     # Authentication & user management
│   │   ├── models.py             # User SQLAlchemy model
│   │   ├── schemas.py            # Pydantic schemas: UserBase, UserCreate, UserResponse, LoginRequest
│   │   ├── crud.py               # User CRUD operations + get_user_or_404 helper
│   │   ├── router.py             # User & auth endpoints
│   │   ├── hashing.py            # Password hashing: hash_pass(), ver_pass()
│   │   └── jwt.py                # JWT token creation & verification + oauth2_scheme
│   ├── transactions/             # Transactions module
│   │   ├── models.py             # Transaction SQLAlchemy model (Enum type, timezone-aware created_at)
│   │   ├── schemas.py            # TransactionBase, TransactionCreate, TransactionResponse, TransactionType
│   │   ├── crud.py               # Transaction CRUD + get_transaction_or_404 (ownership enforced)
│   │   └── router.py             # Transaction endpoints (JWT protected)
│   ├── categories/               # Categories module
│   │   ├── models.py             # Category model — user_id nullable (NULL = default category)
│   │   ├── schemas.py            # CategoryBase, CategoryCreate, CategoryResponse
│   │   ├── crud.py               # CRUD operations + get_categ_or_404 helper
│   │   └── router.py             # Category endpoints (JWT protected)
│   ├── core/
│   │   └── config.py             # App configuration via pydantic-settings
│   └── db/
│       └── database.py           # SQLAlchemy engine, SessionLocal, Base, get_db()
├── scripts/
│   └── seed_categories.py        # Seeds default categories into the database
├── test/
│   ├── conftest.py               # pytest fixtures (SQLite in-memory + StaticPool)
│   └── test_auth.py              # Auth tests
├── alembic/                      # Database migration files
├── docker-compose.yml
├── requirements.txt
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
| GET | `/auth/users/me` | Get current user profile | ✅ JWT |
| PUT | `/auth/users/me` | Update current user | ✅ JWT |
| DELETE | `/auth/users/me` | Delete current user | ✅ JWT |

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

---

## 🧠 Key Design Decisions

| Decision | Why |
|----------|-----|
| 404 instead of 403 on ownership checks | Returning 403 confirms the resource exists — an attacker can enumerate IDs. 404 reveals nothing. |
| Validation logic in CRUD, not routers | Routers handle HTTP concerns; business logic belongs in the service layer. Easier to test and reuse. |
| `bcrypt==4.0.1` pinned | passlib is incompatible with bcrypt 5.x — silent auth failures in production without this pin. |
| `DateTime(timezone=True)` on `created_at` | Timezone-naive datetimes cause subtle bugs when servers or users are in different timezones. |
| SQLite in tests, PostgreSQL in production | Tests run without Docker (faster CI); StaticPool forces in-memory SQLite to reuse one connection so setup tables stay visible. |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone https://github.com/jellalis/personal_fin_tracker.git
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
# Windows
$env:PYTHONPATH="src"; pytest test/ -v

# Mac/Linux
PYTHONPATH=src pytest test/ -v
```

Tests use an SQLite in-memory database — no Docker needed to run the test suite.

---

## 🔒 Security Notes

- Passwords hashed with bcrypt via passlib — never stored as plain text
- Identical 401 responses for wrong password and unknown email — prevents email enumeration
- JWT tokens required for all user, category, and transaction endpoints (except `POST /auth/users` and `POST /auth/login`)
- `.env` excluded from version control via `.gitignore`
- `bcrypt==4.0.1` pinned — passlib incompatible with bcrypt 5.x
- Duplicate email check enforced at CRUD layer — returns 409 Conflict

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
| pytest infrastructure + auth tests | ✅ Complete |
| Categories CRUD + routing + seeding | ✅ Complete |
| Transactions CRUD + routing | ✅ Complete |
| Expanded test coverage | 🔄 In Progress |
| CI/CD (GitHub Actions) | 🔲 Planned |
| Live deployment (Render + Neon) | ✅ Complete |
| Budgets CRUD + routing | 🔲 Planned |

---

## 📄 License

MIT
