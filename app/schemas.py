from pydantic import BaseModel, EmailStr, UUID4, Field
from datetime import datetime
from enum import IntEnum
from typing import List

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID4
    datetime_created: datetime

    class config:
        orm_mode= True # used by sqlalchemy for lazy loading
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: UUID4 | None = None



class PostBase(BaseModel):
    title: str
    content: str
    

class PostIn(PostBase):
    published: bool = True


class PostOwner(BaseModel):
    id: UUID4
    name: str

    class Config:
        orm_mode = True

class PostVoter(BaseModel):
    id: UUID4
    name: str

    class Config:
        orm_mode = True
        
class PostOut(PostBase):
    id: int
    datetime_created: datetime
    owner: PostOwner

    class config:
        orm_mode = True
    
class PostWithVotesOut(BaseModel):
    Post: PostOut
    votes_count: int
    voters: List[PostVoter]
    
    class config:
        orm_mode = True
    
class PostWithVotersOut(BaseModel):
    Post: PostOut
    votes_count: int
    voters: List[PostVoter]

    class Config:
        orm_mode = True
 



class VoteType(IntEnum):
    """Enum for vote types"""
    DOWN = 0
    UP = 1
    
class Vote(BaseModel):
    post_id: int = Field(
        description = "The ID of the post being voted on"
    )
    vote_direction: VoteType = Field(
        description="Vote direction: 0 for downvote, 1 for upvote"
    )
    
    class Config:
        """Pydantic model configuration"""
        title = "Vote Schema"
        description = "Schema for creating or updating a vote on a post"
        json_schema_extra = {
            "example": {
                "post_id": 1,
                "vote_direction": 1
            }
        }