from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import settings

# create_engine() builds the connection pool to PostgreSQL
# The DATABASE_URL is assembled dynamically in core/config.py from .env variables
engine = create_engine(settings.DATABASE_URL)  # συνδεση της python με την postgres

# sessionmaker() creates a factory that produces database sessions on demand
# autocommit=False → we control when to save changes (we call db.commit() explicitly)
# autoflush=False  → SQLAlchemy won't auto-send pending changes to DB before a query
# bind=engine      → links every session to our PostgreSQL connection pool
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # οριζω ρυθμισεις για την sql alchemy

# Base is the parent class that ALL SQLAlchemy models must inherit from
# It lets SQLAlchemy (and Alembic) discover all tables defined in the project
class Base(DeclarativeBase):
    pass

# get_db() is a FastAPI dependency — it opens a fresh DB session for each incoming request
# The 'yield' pattern means:
#   - code before yield   → runs BEFORE the route handler
#   - yield db            → passes the session to the route (via Depends)
#   - code after yield    → runs AFTER the route finishes (cleanup)
# The 'with' block guarantees the session is always closed, even if an error occurs mid-request
def get_db():
    with SessionLocal() as db:
        yield db
