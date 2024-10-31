from fastapi import FastAPI, Response, status, HTTPException, Depends

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from pydantic import BaseModel, EmailStr

from typing import Optional
from datetime import datetime
import uuid

from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

for i in range(10):
    try:
        conn = psycopg2.connect(
            host='localhost', port='5432', user='postgres',
            password='Daf28876#@', dbname='social-media-db', cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection created successfully")
        break
    except psycopg2.Error as error:
        print("Connection to database failed")
        print("ERROR: ", error)
        time.sleep(2)



class Post(BaseModel):
    # id: Optional[uuid.UUID] = None
    title: str
    content: str
    published: bool = True
    # datetime_created: Optional[datetime] = None

class User(BaseModel):
    # id: Optional[int] = None
    email: EmailStr
    name: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users")
async def create_user(user: User, db: Session = Depends(get_db)):
    new_user =  models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "date": new_user
    }


@app.get("/users/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    # print(user)
    return {
        "data": user
    }


@app.get("/posts", status_code=status.HTTP_201_CREATED)
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {
        "data": posts
    }

@app.get("/posts/{id}")
async def get_post_by_id(id: uuid.UUID, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist!"
        ) 

    return {
        "data": post
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {
        "data": new_post
    }
    

@app.delete("/posts/{id}")
async def delete_post(id: uuid.UUID, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
        
    post.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post_by_id(id: uuid.UUID, updated_post: Post, db: Session = Depends(get_db)):    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found"
        )
        
    post = post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()    
    return {
        "message": "Post Updated Successfully",
        "data": post_query.first()
    }


