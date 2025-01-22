from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from typing import List
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError

from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/by-email/", response_model=schemas.UserOut)
def get_user_by_email(email: schemas.EmailStr, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email: {email} doesn't exist!"
        )
    return user

@router.get("/{id}", response_model=schemas.UserOut)
async def get_user_by_id(id: UUID4, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist!"
        )
    return user

    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    # hash the password -> user.password
    hashed_password =  utils.hash(user.password)
    user.password = hashed_password
    new_user =  models.User(**user.model_dump())
    try: 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user 
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email does already exist!"
        )



