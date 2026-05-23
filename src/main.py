from auth.router import router as auth_router
from fastapi import FastAPI
from categories.router import router as categories_router
app=FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(categories_router)