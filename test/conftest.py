from sqlalchemy.orm import Session
import pytest
from sqlalchemy import create_engine
from db.database import Base
from sqlalchemy.orm import sessionmaker
# Ορίζουμε test database (SQLite in-memory)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Fixture 1: Δημιουργεί/σβήνει tables — μια φορά για όλα τα tests
@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    
# Fixture 2: Δίνει καθαρό session σε κάθε test
@pytest.fixture(scope="function")
def db_session(db_engine):
    with SessionLocal() as db:
        yield db
        db.rollback()
    