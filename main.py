from fastapi import FastAPI,APIRouter
from models import User
from db import Database
from rounters import router

def create_app()->None:
    app = FastAPI(
        title="User",
        version='0.0.1',
        description="FastAPI CRUD Asyncpg",
        debug=True,
    )
    app.include_router(router)
    return app


app  = create_app()