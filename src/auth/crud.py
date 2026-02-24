from sqlalchemy.orm import Session
from auth.models import User
from auth.schemas import UserCreate,UserResponse

def create_user(db: Session , user_data : UserCreate):
    new_user=User(name=user_data.name,email=user_data.email,hashed_password=user_data.password)#creation of user with schemas infos
    db.add(new_user)#adding new user to db 
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db:Session, user_id :int):
    user=db.query(User).filter(User.id==user_id).first()
    return user
def update_user(db:Session,user_id: int, user_data: UserCreate):
    user_up=get_user(db,user_id)
    user_up.name=user_data.name
    user_up.email=user_data.email
    user_up.password=user_data.password 
    db.commit()
    db.refresh()
    return user_up
def delete_user(db:Session,user_id: int):
    user_del=get_user(db,user_id)
    db.delete(user_del)
    db.commit()
def get_user_by_email(db:Session,email:str):
    user=db.query(User).filter(User.email==email).first()
    return user
    
    
    
    
