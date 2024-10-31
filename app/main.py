from fastapi import FastAPI, Response, status, HTTPException, Depends

import psycopg2
from psycopg2.extras import RealDictCursor
import time
import uuid

from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session 
from typing import List

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



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.Post)
async def get_post_by_id(id: uuid.UUID, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} does not exist!"
        ) 
        
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

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


@app.put("/posts/{id}", response_model=schemas.Post)
async def update_post_by_id(id: uuid.UUID, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found"
        )
        
    post = post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()    
    
    return post_query.first()


