from auth.crud import create_user, delete_user, update_user, get_user, get_user_by_email, get_user_or_404
from auth.schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from db.database import get_db
from auth.jwt import create_tok, oauth2_scheme, verify_tok
from auth.hashing import ver_pass
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# POST /auth/users — register a new user
# No JWT required — this is the registration endpoint
@router.post("/users", response_model=UserResponse, status_code=201)
def post_router(user_data: UserCreate, db: Session = Depends(get_db)):
    post_r_user = create_user(db, user_data)
    return post_r_user

# GET /auth/users/me — fetch the currently logged-in user's profile
# user_id comes from the JWT token — not from the URL
@router.get("/users/me", response_model=UserResponse)
def get_router(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_tok(token)
    user_id = int(payload["sub"])
    return get_user_or_404(db, user_id)

# DELETE /auth/users/me — permanently delete the currently logged-in user
@router.delete("/users/me", response_model=UserResponse)
def delete_router(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_tok(token)
    user_id = int(payload["sub"])
    return delete_user(db, user_id)

# PUT /auth/users/me — update the currently logged-in user's information
@router.put("/users/me", response_model=UserResponse)
def update_router(user_data: UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_tok(token)
    user_id = int(payload["sub"])
    return update_user(db, user_id, user_data)

# POST /auth/login — returns a JWT token if credentials are valid
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_by_email = get_user_by_email(db, form_data.username)
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