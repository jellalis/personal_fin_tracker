from categories.crud import create_category,get_categories,get_category,delete_category,get_categ_or_404
from categories.schemas import CategoryBase,CategoryResponse,CategoryCreate
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException
from db.database import get_db


from auth.jwt import oauth2_scheme,verify_tok
router=APIRouter()

@router.post("/categories",response_model=CategoryResponse)

def post_router(category_data:CategoryCreate,db:Session=Depends(get_db),token: str=Depends(oauth2_scheme)):
    payload = verify_tok(token)
    user_id = int(payload["sub"])
    new_categ = create_category(db, category_data, user_id)
   
    return new_categ
@router.get("/categories",response_model=list[CategoryResponse])
def get_routers(db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = verify_tok(token)
    user_id = payload["sub"]
    categories=get_categories(db,user_id)
    return categories
@router.get("/categories/{category_id}",response_model=CategoryResponse)
def get_router(category_id:int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    category=get_categ_or_404(db,category_id)
    return category
@router.delete("/categories/{category_id}")
def del_router(category_id:int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    del_cat=delete_category(db,category_id)
    return  "category deleted"