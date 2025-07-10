from fastapi import FastAPI
from app.api.routers import auth_routes, user_routes, todo_routes

def include_routers(app):
    app.include_router(user_routes.router)
    app.include_router(todo_routes.router)
    app.include_router(auth_routes.router)
