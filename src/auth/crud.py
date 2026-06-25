from sqlalchemy.orm import Session
from auth.models import User
from auth.schemas import UserCreate,UserResponse
from fastapi import APIRouter, Depends,HTTPException
from auth.hashing import hash_pass

def create_user(db: Session , user_data : UserCreate):
    # hash_pass() converts the plain password to a bcrypt hash before storing
    # We pass the hash to the model, never the raw password
    if get_user_by_email(db,user_data.email):
        raise HTTPException(status_code=409, detail="A user with this email already exists")
    
    new_user=User(name=user_data.name,email=user_data.email,hashed_password=hash_pass(user_data.password))  # creation of user with schemas infos
    
            
    db.add(new_user)     # stages the new user for insertion (not written to DB yet)
    db.commit()          # flushes the staged change and writes it to the database
    db.refresh(new_user) # re-reads the row from DB so new_user now has the auto-generated id
    return new_user

def get_user(db:Session, user_id :int):
 
    user=db.query(User).filter(User.id==user_id).first()
    return user

def update_user(db:Session,user_id: int, user_data: UserCreate):
    user_up=get_user_or_404(db,user_id)
    existing_user=get_user_by_email(db,user_data.email)
    if existing_user != user_up and existing_user is not None:
        raise HTTPException(status_code=409, detail="A user with this email already exists")

    user_up.name=user_data.name
    user_up.email=user_data.email
    user_up.hashed_password=hash_pass(user_data.password)
    db.commit()
    db.refresh(user_up)
    return user_up

def delete_user(db:Session,user_id: int):
    user_del=get_user_or_404(db,user_id)
    db.delete(user_del) 
    db.flush()
    db.expunge(user_del)
    db.commit() 
    return user_del

def get_user_by_email(db:Session,email:str):
    # Used at login to look up a user by their email address before verifying the password
    user=db.query(User).filter(User.email==email).first()
    return user

def get_user_or_404(db:Session ,user_id: int ):
    # Reusable helper: fetches a user OR raises HTTP 404 if they don't exist
    # Use this in routes instead of get_user() to avoid repeating the same if-not-user check everywhere
    user=get_user(db,user_id)
    if not user :
        raise HTTPException(status_code=404, detail="no user with this id")
    return user
