from categories.crud import create_category
from categories.schemas import CategoryCreate
from db.database import SessionLocal
import auth.models  # ← κάνει γνωστό το users table στο SQLAlchemy
default_cat=["food","supermarket","gifts","subscriptions","bills","entertainment "]

db = SessionLocal()



for name in default_cat:
    category_data=CategoryCreate(name=name)
    create_category(db,category_data,None)
db.close()