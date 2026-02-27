from sqlalchemy.orm import Session
import pytest
from sqlalchemy import create_engine
from db.database import Base
from auth.crud import create_user
from auth.schemas import UserCreate 
from sqlalchemy.orm import sessionmaker, DeclarativeBase

def test_create_user(db_session):
    test_user=UserCreate(name="", email="", password ="")
    result=create_user(db_session,test_user)
    assert result.name == ""
    assert result.email ==""