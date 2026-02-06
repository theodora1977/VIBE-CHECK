from pydantic import BaseModel
from typing import List

class BusinessCreate(BaseModel):
    name: str
    category: str
    location: str


class Business(BaseModel):
    id: int
    name: str
    category: str
    location: str
    vibe_score: float

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    user_id: int
    business_id: int
    content: str


class Review(BaseModel):
    id: int
    user_id: int
    business_id: int
    content: str
    vibe_score: float
    sentiment: str
    keywords: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
