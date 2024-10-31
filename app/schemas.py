from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True    

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: UUID4
    datetime_created: datetime
    
    class config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    datetime_created: datetime
    
    class config:
        orm_mode = True
