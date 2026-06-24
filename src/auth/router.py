from auth.crud import create_user,delete_user,update_user,get_user,get_user_by_email,get_user_or_404
from auth.schemas import UserCreate,UserResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,HTTPException
from db.database import get_db
from auth.jwt import create_tok
from auth.hashing import ver_pass,hash_pass
from auth.schemas import LoginRequest
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter()

# POST /auth/users — register a new user
# response_model=UserResponse controls what fields are returned (hides the password field)
# Depends(get_db) injects a database session automatically — we never create one manually in routes
@router.post("/users",response_model=UserResponse,status_code=201)
def post_router(user_data :UserCreate,db:Session=Depends(get_db)):
        
        post_r_user=create_user(db,user_data)
        return post_r_user


# GET /auth/users/{user_id} — fetch a single user by their id
# {user_id} in the path is a path parameter — FastAPI parses it from the URL automatically
@router.get("/users/{user_id}",response_model=UserResponse)
def get_router(user_id:int,db:Session=Depends(get_db)):
    user_get=get_user_or_404(db,user_id)  
    return user_get

# DELETE /auth/users/{user_id} — permanently delete a user from the database
@router.delete("/users/{user_id}",response_model=UserResponse)
def delete_router(user_id:int,db:Session=Depends(get_db)):
    return delete_user(db, user_id)


# PUT /auth/users/{user_id} — update an existing user's information
@router.put("/users/{user_id}",response_model=UserResponse)
def update_router(user_data :UserCreate,user_id:int,db:Session=Depends(get_db)):
        return update_user(db,user_id,user_data)

# POST /auth/login — returns a JWT token if credentials are valid
# OAuth2PasswordRequestForm is the standard OAuth2 login form — Swagger UI uses it for the "Authorize" button
# It uses 'username' as the field name (OAuth2 standard), even though our app uses email addresses
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
        user_by_email = get_user_by_email(db, form_data.username)  # ← username αντί για email (OAuth2 standard)
        # Security decision: return identical 401 for wrong password AND user not found
        # Giving different errors would allow attackers to enumerate valid email addresses 
        if not user_by_email:
            raise HTTPException(status_code=401, detail="wrong detail")
        ok_pass = ver_pass(form_data.password, user_by_email.hashed_password)
        if not ok_pass:
            raise HTTPException(status_code=401, detail="wrong detail")
        token_created = create_tok(user_by_email.id)
                # token_type "bearer" tells clients how to send the token:
                # Authorization: Bearer <token>
        return {"access_token": token_created, "token_type": "bearer"}
            

