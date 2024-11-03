from .. import models, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from typing import List
from ..database import get_db
import uuid

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post_by_id(id: uuid.UUID, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} does not exist!"
        )
        
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
async def create_post(post: schemas.PostIn, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

@router.put("/{id}", response_model=schemas.PostOut)
async def update_post(id: uuid.UUID, updated_post: schemas.PostIn, db: Session = Depends(get_db)):    
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
    

@router.delete("/{id}")
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




