from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True    

class PostIn(PostBase):
    pass


class PostOut(PostBase):
    id: UUID4
    datetime_created: datetime
    
    class config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    datetime_created: datetime
    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str