import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from db.database import Base
from auth.models import User
from budget.models import Budget
from categories.models import Category
from transactions.models import Transaction
from main import app
from db.database import get_db
from starlette.testclient import TestClient
from auth.crud import create_user
from auth.jwt import create_tok
from auth.schemas import UserCreate
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

@pytest.fixture
def client(db):
    app.dependency_overrides[get_db]=lambda:db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(db):
    user_data=UserCreate(
    name="Panos",
    email="Panos@gmail.com",
    password="Panos"        
    )
    created=create_user(db,user_data)
    created_token=create_tok(created.id)
    return {"Authorization": f"Bearer {created_token}"}
