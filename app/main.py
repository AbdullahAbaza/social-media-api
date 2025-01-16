from fastapi import FastAPI
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# from . import models
# from .database import engine

# import logging
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


## --> not needed if we use alembic database migration tool
# def create_db_and_tables():  
#     models.Base.metadata.create_all(bind=engine)

    
# app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})
app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello From FastAPI!."}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
