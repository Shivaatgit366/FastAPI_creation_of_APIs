from datetime import date
from typing import Optional
from pydantic import BaseModel, HttpUrl
from pydantic.schema import datetime


class UserBase(BaseModel):
    email: str
    password: str


class ShorturlBase(BaseModel):
    original_url: HttpUrl


class Short_Url(ShorturlBase):
    created_date: date
    short_url: str

    class Config:
        orm_mode = True


class Clicks(BaseModel):
    date: date
    short_url: str
    click_count: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ShortUrlCount(BaseModel):
    created_date: date
    short_urls_count: int

