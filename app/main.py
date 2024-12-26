from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote

import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


# def create_db_and_tables():  # --> not needed if we use alembic database migration tool
#     models.Base.metadata.create_all(bind=engine)
    
app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
