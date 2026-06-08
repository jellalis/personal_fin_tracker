import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from db.database import Base
from auth.models import User
from budget.models import Budget
from categories.models import Category
from transactions.models import Transaction

TEST_DATABASE_URL = "sqlite://"

engine= create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    session=TestingSessionLocal()

    try:
        yield session
    finally:
        session.close() 
        Base.metadata.drop_all(bind=engine)
        