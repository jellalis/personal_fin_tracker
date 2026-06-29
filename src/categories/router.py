from categories.crud import create_category, get_categories, get_category, delete_category, get_categ_or_404
from categories.schemas import CategoryBase, CategoryResponse, CategoryCreate
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from db.database import get_db

# oauth2_scheme extracts the Bearer token from the Authorization header on every request
# verify_tok() decodes the token and returns the payload (contains user_id as "sub")
from auth.jwt import oauth2_scheme, verify_tok

router = APIRouter()

# POST /categories — create a new category owned by the logged-in user
@router.post("/categories", response_model=CategoryResponse, status_code=201)
def post_router(category_data: CategoryCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_tok(token)    # decode and validate the JWT — raises 401 if invalid or expired
    user_id = int(payload["sub"])  # "sub" is always a string in JWT standard — convert to int for the DB
    new_categ = create_category(db, category_data, user_id)
    return new_categ

# GET /categories — return all categories visible to the logged-in user (own + defaults)
@router.get("/categories", response_model=list[CategoryResponse])
def get_routers(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_tok(token)
    user_id = int(payload["sub"])
    categories = get_categories(db, user_id)
    return categories

# GET /categories/{category_id} — fetch a single category by its id
# JWT verified — expired or tampered tokens are rejected before hitting the DB
@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_router(category_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_tok(token)
    user_id = int(payload["sub"])
    
    category = get_categ_or_404(db, category_id,user_id)
    return category

# DELETE /categories/{category_id} — delete a category owned by the logged-in user
# JWT verified + ownership enforced in CRUD layer (404 if not owner or category doesn't exist)
@router.delete("/categories/{category_id}", response_model=CategoryResponse)
def del_router(category_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_tok(token)
    user_id = int(payload["sub"])
    del_cat = delete_category(db, category_id, user_id)
    return del_cat