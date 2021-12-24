from typing import Optional
from pydantic import BaseModel
from pydantic.schema import datetime


class UserBase(BaseModel):
    email: str
    password: str


class ShorturlBase(BaseModel):
    created_date: datetime
    user_id: int
    original_url: str


class Click(BaseModel):
    date: datetime
    short_url: str
    click_count: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

