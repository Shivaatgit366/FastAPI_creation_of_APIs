from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from typing import List


app = FastAPI()


class My_blog(BaseModel):
    title: str
    body: str


class relation_blog(My_blog):
    # since it is the extension/subclass of "My_blog", no need to mention attributes again.
    class Config:  # we made another response model by adding "class config".
        orm_mode = True


class Show_user(BaseModel):  # this is the desired response model which will be used inside the decorator.
    name: str
    email: str
    blog: List[relation_blog] = []

    # remember to add class config, orm mode = True.
    class Config:
        orm_mode = True


class Show_blog(BaseModel):
    # in the response model, we can add "user" attribute made from relationship.
    # Type of the "user" is also a response model of another table.
    # It should be kept above since python executes the code line by line.
    title: str
    body: str
    user: Show_user

    class Config:
        orm_mode = True


class Create_user(BaseModel):  # new model is created. It will be used for request body to create user table.
    name: str
    email: str
    password: str


# "OAuth2PasswordBearer" library takes "username" as the identifier, so we are giving username for the input.
class Login(BaseModel):  # username means the email of the user in this example.
    username: str
    password: str


# create these two below models for the token creation.
# Token and TokenData are the pydantic models which will be created.
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


