from sqlalchemy import Column, Integer, String,ForeignKey
from db.database import Base  # ⚠️ Always import Base from here — never from src.db.database

# Category is a SQLAlchemy ORM model — it maps directly to the 'categories' table in PostgreSQL
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # ForeignKey("users.id") creates a link to the 'id' column in the 'users' table
    # nullable=True is intentional — NULL means this is a default category visible to ALL users
    # Design decision: user_id=NULL → "belongs to everyone", user_id=<int> → "belongs to that user only"
    user_id=Column(Integer,ForeignKey("users.id"),nullable=True)
