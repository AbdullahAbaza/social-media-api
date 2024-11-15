from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user,auth


def create_db_and_tables():
    models.Base.metadata.create_all(bind=engine)
    
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)

