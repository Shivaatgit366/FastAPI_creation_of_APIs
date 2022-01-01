from pydantic import BaseModel
from typing import Optional
from pydantic.schema import date


class AuthorBase(BaseModel):
    email: str
    password: str


class BlogBase(BaseModel):
    title: str
    body: str


class BlogsOut(BaseModel):
    author_id: int
    blog_title: str

    class Config:
        orm_mode = True


class BlogsCreate(BaseModel):
    author_id: int
    blog_id: str
    published_date: date
    title: str

    class Config:
        orm_mode = True


class GetOneBlog(BaseModel):
    blog_id: str
    title: str
    body: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: Optional[str] = None
