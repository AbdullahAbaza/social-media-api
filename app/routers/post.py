from typing import List, Optional
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from sqlalchemy import func, select
from sqlalchemy.types import JSON
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

class SortDirection(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/", response_model=List[schemas.PostWithVoteCountOut])
async def get_posts(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user),
    skip: int = 0,
    limit: int = Query(default=10, le=100), 
    search: Optional[str] = None,
    sort_direction: SortDirection = SortDirection.desc
    ):

    # Base query with vote count
    posts_query = db.query(models.Post, 
                           func.count(models.Vote.post_id).label("votes_count")
        ).outerjoin(models.Vote, models.Vote.post_id == models.Post.id)\
            .group_by(models.Post.id)
    
    # Filter Posts that are published only
    posts_query = posts_query.filter(models.Post.published.is_(True))
    
    # Apply search filter if provided
    if search:
        posts_query = posts_query.filter(
            func.lower(models.Post.title).contains(func.lower(search))
        )
        
    # Apply Sorting 
    order_by = models.Post.datetime_created.desc() if sort_direction == SortDirection.desc\
        else models.Post.datetime_created.asc()
    
    # Apply Pagination
    posts_query = posts_query.order_by(order_by)\
                        .limit(limit)\
                        .offset(skip)
                            

    # # Debugging: Print the raw SQL
    # print(str(posts_query.statement))
    
    
    # Execute Query and return the result
    posts = posts_query.all()
    return posts


@router.get("/votes/{post_id}", response_model=schemas.PostWithVotersOut)
async def get_post_with_votes(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
    ):
    
    # Vote
    
    # Fetch the post
    post_query = db.query(
        models.Post
        
        ).filter(models.Post.id == post_id)
    
        
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist!"
        )
        
    # check user authrization to view not puplished posts 
    if not post.published and post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorizerd to perform requested action"
        )

    # Lazily load votes and voters 
    
    votes_count = len(post.votes)
    voters = [
        {"id": vote.user.id, "name": vote.user.name} for vote in post.votes if vote.user
    ]

    return {
        "Post": post,
        "votes_count": votes_count,
        "voters": voters,
    }



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




