from sqlalchemy.orm import Session
import pytest
from sqlalchemy import create_engine
from db.database import Base
from sqlalchemy.orm import sessionmaker

# Tests use SQLite in-memory instead of PostgreSQL
# Benefits: fast (no network), no Docker needed, fully isolated (deleted after tests)
# Limitation: SQLite doesn't support all PostgreSQL features — complex queries may behave differently
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Fixture 1: Δημιουργεί/σβήνει tables — μια φορά για όλα τα tests
# scope="session" → runs ONCE for the entire test run (not once per test)
# create_all() creates every table defined in SQLAlchemy models (they must be imported first)
# drop_all() at the end cleans up — each test run starts with a fresh schema
@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

# Fixture 2: Δίνει καθαρό session σε κάθε test
# scope="function" → runs once PER test function — each test gets its own session
# db.rollback() after the test undoes all changes made during that test
# This prevents tests from polluting each other's data (test isolation)
@pytest.fixture(scope="function")
def db_session(db_engine):
    with SessionLocal() as db:
        yield db
        db.rollback()  # undo all DB changes made during this test

# override_get_db replaces the real get_db() dependency when running tests
# This makes FastAPI routes use the SQLite test session instead of the real PostgreSQL session
# To activate it in a test: app.dependency_overrides[get_db] = override_get_db
def override_get_db():
    with SessionLocal() as db:
        yield db
