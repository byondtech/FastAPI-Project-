
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password: str

class Posts(BaseModel):
    title: str
    content: str
    published: bool = True

class Post_base(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(Post_base):
    pass

class Post(Post_base):
    id: int
    created_at: datetime 
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class get_posts(BaseModel):
    title: str
    content: str
    published: bool = True
    id: int
    created_at: datetime 
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class Postout(BaseModel):
    Post: get_posts
    votes: int

    class Config:
        orm_mode = True


    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: int
    @validator('dir')
    def check_value(cls, v):
        if v not in (0, 1):
            raise ValueError('Value must be 0 or 1')
        return v