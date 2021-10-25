from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class My_blog(BaseModel):
    title: str
    body: str


class Show_blog(BaseModel):  # this is the desired model which can be used as the response model.
    title: str
    body: str

    class Config:
        orm_mode = True

