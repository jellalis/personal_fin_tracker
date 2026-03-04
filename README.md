# 💰 Personal Finance Tracker API

A RESTful API built with Python and FastAPI for tracking personal finances. This project demonstrates core backend engineering skills including REST API design, PostgreSQL database management, SQLAlchemy ORM, and Docker containerization.

---

## 🛠️ Tech Stack

- **Python** - Core language
- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM (Object Relational Mapper)
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Docker & Docker Compose** - Containerization
- **passlib[bcrypt]** - Password hashing

---

## 📁 Project Structure

```
personal_fin_tracker/
├── alembic/                  # Database migration files
├── src/
│   ├── auth/                 # User management & authentication
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── crud.py           # Database operations
│   │   ├── router.py         # API endpoints
│   │   └── hashing.py        # Password hashing utilities
│   ├── core/
│   │   └── config.py         # App configuration (env variables)
│   ├── db/
│   │   └── database.py       # Database connection
│   └── main.py               # Application entry point
├── .env.example              # Environment variables template
├── docker-compose.yml        # Docker configuration
├── requirements.txt          # Python dependencies
└── README.md
```

---

## ⚙️ Prerequisites

Make sure you have the following installed:

- [Python 3.10+](https://www.python.org/)
- [Docker & Docker Compose](https://www.docker.com/)
- [Git](https://git-scm.com/)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/personal_fin_tracker.git
cd personal_fin_tracker
```

### 2. Create and activate virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\Activate.ps1

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your values
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=finance_tracker
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Start the database with Docker

```bash
docker-compose up -d
```

### 6. Run database migrations

```bash
alembic upgrade head
```

### 7. Start the API server

```bash
$env:PYTHONPATH="src"; uvicorn src.main:app --reload  # Windows
PYTHONPATH=src uvicorn src.main:app --reload           # Mac/Linux
```

The API will be available at `http://127.0.0.1:8000`

---

## 📖 API Documentation

FastAPI automatically generates interactive documentation. Once the server is running, visit:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 🔗 API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users` | Create a new user (register) |
| `GET` | `/users/{user_id}` | Get user by ID |
| `PUT` | `/users/{user_id}` | Update user details |
| `DELETE` | `/users/{user_id}` | Delete a user |

### Auth (in progress)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/login` | Login and receive JWT token |

### Example Request — Create User

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword"
  }'
```

### Example Response

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "enabled": true
}
```

> ⚠️ Passwords are **never** returned in API responses.

---

## 🗄️ Database Schema

The database consists of 4 tables:

- **users** - User accounts
- **transactions** - Financial transactions
- **categories** - Transaction categories
- **budgets** - Budget tracking

---

## 🔒 Security Notes

- Passwords are hashed with bcrypt via passlib (never stored as plain text)
- The `.env` file is excluded from version control via `.gitignore`
- Always use `.env.example` as a template — never commit real credentials
- JWT tokens will be used for authentication (in progress)

---

## 📌 Status

🚧 **In Progress** — Currently implementing:
- [x] Database schema & migrations
- [x] User CRUD endpoints with proper error handling (404 for missing users, 409 for duplicate email)
- [x] Password hashing (bcrypt via passlib) — `src/auth/hashing.py`
- [ ] Login endpoint (`POST /auth/login`) — **next step**
- [ ] JWT token generation & verification
- [ ] Protected endpoints (require valid JWT token)
- [ ] Transactions endpoints
- [ ] Categories endpoints
- [ ] Budgets endpoints

---

## 🗺️ Current State (Session Notes)

### Last session summary
- Implemented `get_user_or_404` helper in `crud.py` — reusable 404 check for all endpoints that need a `user_id`
- Fixed `db.refresh(user_up)` in `update_user`
- Fixed field name `hashed_password` in `update_user`
- Created `src/auth/hashing.py` with `hash_pass(password)` and `ver_pass(password, hashed)` using passlib/bcrypt
- Updated `create_user` in `crud.py` to hash passwords before storing

### Next session — start here
1. Create `POST /auth/login` endpoint in `src/auth/router.py`
2. Use `ver_pass()` from `hashing.py` to verify the password
3. If valid → generate JWT token and return it
4. Install `python-jose` for JWT support

---

## 📄 License

MIT License