from auth.crud import create_user,delete_user,update_user,get_user,get_user_by_email
from auth.schemas import UserCreate,UserResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,HTTPException
from db.database import get_db

router=APIRouter()

@router.post("/users",response_model=UserResponse)

def post_router(user_data :UserCreate,db:Session=Depends(get_db)):
    if get_user_by_email(db,user_data.email):
        raise HTTPException(status_code=409, detail="there is also a same email")

    else :
        post_r_user=create_user(db,user_data)
    
    return post_r_user
    
    
@router.get("/users/{user_id}",response_model=UserResponse)
def get_router(user_id:int,db:Session=Depends(get_db)):
    get_r_user=get_user(db,user_id)
    return get_r_user

@router.delete("/users/{user_id}",response_model=UserResponse)
def delete_router(user_id:int,db:Session=Depends(get_db)):
    del_r_user=delete_user(db,user_id)
    return del_r_user



@router.put("/users/{user_id}",response_model=UserResponse)
def update_router(user_data :UserCreate,user_id:int,db:Session=Depends(get_db)):
    upd_r_user=update_user(db,user_id,user_data)
    return upd_r_user
    