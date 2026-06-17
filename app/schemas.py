from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email : EmailStr
    name : str
    password : str
    
class UserResponse(BaseModel):
    id: int
    email : EmailStr
    name : str
    class Config:
        orm_mode = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int

class PostBase(BaseModel):
    title : str
    content: str
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        orm_mode = True

class Vote(BaseModel):
    id_post: int
    dir: bool

