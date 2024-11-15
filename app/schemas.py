from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID4
    datetime_created: datetime
    
    
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
    published: bool = True

class PostIn(PostBase):
    pass


class PostOut(PostBase):
    id: int
    datetime_created: datetime
    owner_id: UUID4
    owner: UserOut
    
    class config:
        orm_mode = True


