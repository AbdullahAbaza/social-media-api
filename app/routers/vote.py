from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
               current_user: models.User = Depends(oauth2.get_current_user)):
    # 1) check if post with id exist
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post With id: {vote.post_id} does not exist"
        )
    
    # build base vote query
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
        
    # add vote 
    if (vote.vote_direction == 1): 
        # check if vote already exist
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"user with ID: {current_user.id} has already voted on post: {vote.post_id}")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "succesfully added vote"}
    
    # delete a vote
    else:
        # check if vote already exist
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "succesfully deleted vote"}
        
        
