from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user), 
    limit: int = 10, skip: int = 0, search: Optional[str] = None
    ):
    
    # Build base query
    posts_query = db.query(models.Post)
    
    # Apply search filter if provided
    if search:
        posts_query = posts_query.filter(
            func.lower(models.Post.title).contains(func.lower(search))
        )
    
    # Apply pagination
    # total = posts_query.count()
    
    posts = posts_query.order_by(models.Post.datetime_created.desc())\
                      .limit(limit)\
                      .offset(skip)\
                      .all()
    
    return posts


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post_by_id(id: int, db: Session = Depends(get_db), 
                         current_user: models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} does not exist!"
        )
        
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
async def create_post(post: schemas.PostIn, 
                      db: Session = Depends(get_db), 
                      current_user: models.User = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

@router.put("/{id}", response_model=schemas.PostOut)
async def update_post(id: int, updated_post: schemas.PostIn, 
                      db: Session = Depends(get_db), 
                      current_user: models.User = Depends(oauth2.get_current_user)):   
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorizerd to perform requested action"
        )
    post = post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
    

@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db), 
                      current_user: models.User = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorizerd to perform requested action"
        ) 
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)




