from auth.crud import create_user,delete_user,update_user,get_user,get_user_by_email,get_404
from auth.schemas import UserCreate,UserResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,HTTPException
from db.database import get_db
from auth.jwt import create_tok
from auth.hashing import ver_pass,hash_pass
from auth.schemas import LoginRequest

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
    user_get=get_404(db,user_id)    
    return user_get

@router.delete("/users/{user_id}",response_model=UserResponse)
def delete_router(user_id:int,db:Session=Depends(get_db)):
    user_get=get_404(db,user_id) 
    del_r_user=delete_user(db,user_id)
    return del_r_user



@router.put("/users/{user_id}",response_model=UserResponse)
def update_router(user_data :UserCreate,user_id:int,db:Session=Depends(get_db)):
    user_get=get_404(db,user_id) 
    upd_r_user=update_user(db,user_id,user_data)
    return upd_r_user

@router.post("/login")
def login(user_data :LoginRequest,db:Session=Depends(get_db)):
    try:
        user_by_email=get_user_by_email(db,user_data.email)
        try:
            ok_pass=ver_pass(user_data.password,user_by_email.hashed_password)
            if ok_pass:
                token_created=create_tok(user_by_email.id)
                return {"access_token": token_created, "token_type": "bearer"}
        except:
            raise HTTPException(status_code=401, detail="wrong details")
        
             
    except:
        raise HTTPException(status_code=401, detail="wrong details")
     