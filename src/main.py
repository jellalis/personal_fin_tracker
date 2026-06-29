# main.py — Entry point of the FastAPI application
# All routers (feature modules) are imported and registered here
# When you add a new feature (e.g. transactions), import its router and call include_router() below

from auth.router import router as auth_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from categories.router import router as categories_router
from transactions.router import router as transactions_router
from reports.router import router as reports_router

# The main app instance — FastAPI creates the HTTP server, Swagger docs, and handles all routing
app = FastAPI()

# CORS middleware — allows the React frontend (e.g. localhost:5173) to call this API
# Without this, the browser blocks all cross-origin requests automatically
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server — add production URL when deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include_router() registers all the routes from a module into the main app
# prefix="/auth" means every route inside auth/router.py will start with /auth
# e.g. POST /users → becomes POST /auth/users, POST /login → becomes POST /auth/login
app.include_router(auth_router, prefix="/auth")

# categories has no prefix, so its routes are at root level (e.g. /categories, /categories/{id})
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(reports_router)