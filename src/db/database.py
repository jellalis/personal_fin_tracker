from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)#συνδεση της python με την postgress
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)# οριζω ρυθμισεις για την sql alchemy 

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db