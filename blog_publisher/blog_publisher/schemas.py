from pydantic import BaseModel
from typing import Optional
from pydantic.schema import date
from blog_publisher.models import StatusTypes


class AuthorBase(BaseModel):
    email: str
    password: str


class BlogCreate(BaseModel):
    title: str
    body: str


# since the user can keep the title and body "empty", we should provide "optional" attributes to the class.
class BlogUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class BlogSummary(BaseModel):
    blog_id: str
    author_id: int
    title: str
    created_date: date
    published_date: Optional[date] = None
    status: StatusTypes

    class Config:
        orm_mode = True


class Blog(BlogSummary):
    body: str


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: Optional[str] = None


