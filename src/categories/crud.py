from sqlalchemy.orm import Session
from categories.models import Category
from categories.schemas import CategoryCreate
from sqlalchemy import or_
from fastapi import HTTPException

#creation of category
def create_category(db: Session, category_data: CategoryCreate, user_id: int):
    new_category=Category(name=category_data.name,user_id= user_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
#get/read categories
def get_categories(db:Session,user_id):
    user=db.query(Category).filter(or_(Category.user_id==user_id,Category.user_id == None)).all()
    return user
#get/read one category
def get_category(db:Session,category_id):
    category=db.query(Category).filter(Category.id==category_id).first()
    return category
#delete category
def delete_category(db:Session,category_id: int):
    category_del=get_categ_or_404(db,category_id)
    db.delete(category_del)
    db.commit()
#check if category is available
def get_categ_or_404(db:Session,category_id:int):
    category=get_category(db,category_id)
    if not category:
        raise HTTPException(status_code=404, detail="no category with this id")    
    return category