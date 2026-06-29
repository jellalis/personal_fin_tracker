# seed_categories.py — Populates the database with default categories
# Run this ONCE after a fresh database setup:
#   $env:PYTHONPATH="src"; python scripts/seed_categories.py
# Running it multiple times will create duplicate default categories

from categories.crud import create_category
from categories.schemas import CategoryCreate
from db.database import SessionLocal
import auth.models  # ← importing this registers the 'users' table with SQLAlchemy's metadata
                    # Required because Category has a ForeignKey to users.id — SQLAlchemy
                    # needs to know about the users table before it can insert into categories

# Default categories — match the frontend Category type exactly so the mapping works
# Frontend expects: food, transport, shopping, entertainment, bills, salary, other
default_cat = ["food", "transport", "shopping", "entertainment", "bills", "salary", "other"]

# Open a database session manually (no FastAPI here, so we don't use get_db())
db = SessionLocal()

# Create each default category with user_id=None → stored as NULL in the DB
# NULL user_id means "belongs to everyone" — see categories/crud.py get_categories()
for name in default_cat:
    category_data=CategoryCreate(name=name)
    create_category(db,category_data,None)  # None → user_id=NULL in the database

# Always close the session when done — releases the connection back to the pool
db.close()
