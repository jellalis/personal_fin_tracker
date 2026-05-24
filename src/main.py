# main.py — Entry point of the FastAPI application
# All routers (feature modules) are imported and registered here
# When you add a new feature (e.g. transactions), import its router and call include_router() below

from auth.router import router as auth_router
from fastapi import FastAPI
from categories.router import router as categories_router

# The main app instance — FastAPI creates the HTTP server, Swagger docs, and handles all routing
app = FastAPI()

# include_router() registers all the routes from a module into the main app
# prefix="/auth" means every route inside auth/router.py will start with /auth
# e.g. POST /users → becomes POST /auth/users, POST /login → becomes POST /auth/login
app.include_router(auth_router, prefix="/auth")

# categories has no prefix, so its routes are at root level (e.g. /categories, /categories/{id})
app.include_router(categories_router)
