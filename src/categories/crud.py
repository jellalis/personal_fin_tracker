from sqlalchemy.orm import Session
from categories.models import Category
from categories.schemas import CategoryCreate
from sqlalchemy import or_
from fastapi import HTTPException

# creation of category
# user_id=None is valid here — the seed script calls this with None for default categories
def create_category(db: Session, category_data: CategoryCreate, user_id: int):
    new_category=Category(name=category_data.name,user_id= user_id)
    db.add(new_category)      # stages the new row for insertion
    db.commit()               # writes it to the database
    db.refresh(new_category)  # re-reads from DB so new_category has the auto-generated id
    return new_category

# get/read categories — returns user's own categories PLUS all default (NULL) categories
def get_categories(db:Session,user_id):
    # or_() builds a SQL OR condition — equivalent to: WHERE user_id = <id> OR user_id IS NULL
    # This gives every user their own categories plus the shared default ones
    user=db.query(Category).filter(or_(Category.user_id==user_id,Category.user_id == None)).all()
    return user

# get/read one category by id
# ⚠️ Known limitation: does NOT verify that the category belongs to the requesting user
# Any authenticated user can fetch any category's details by guessing the id
def get_category(db:Session,category_id):
    category=db.query(Category).filter(Category.id==category_id).first()
    return category

# delete category
# ⚠️ Known limitation: does NOT verify ownership before deleting
# Any authenticated user can delete any category, including other users' categories
def delete_category(db:Session,category_id: int):
    category_del=get_categ_or_404(db,category_id)
    db.delete(category_del)
    db.commit()

# check if category is available — reusable 404 helper (same pattern as get_user_or_404 in auth)
def get_categ_or_404(db:Session,category_id:int):
    category=get_category(db,category_id)
    if not category:
        raise HTTPException(status_code=404, detail="no category with this id")
    return category
