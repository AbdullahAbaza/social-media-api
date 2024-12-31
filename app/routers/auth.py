from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .. import database, models, utils, oauth2, schemas

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
    ):
    
    # 1) Search for the email in the database.
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    # 2) Verify that password is correct.
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
        
    # 3) create a jwt token & return token.
    # encode UUID object to make it JSON compatible or cast uuid as string for faster processing
    # user_id = jsonable_encoder(user.id)
    access_token = oauth2.create_access_token(data = {"user_id": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}