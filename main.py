from typing import Optional
from fastapi import FastAPI

app = FastAPI()  # object is created by calling the FastAPI class.


@app.get("/")  # "/" means base url, original server url. Path or the endpoint is local host itself.
def index():
    return {"data": {"name": "shiva", "age": 26}}


@app.get("/about")  # get function takes the endpoint/path as an argument.
def about():
    return {"data": {"about page": "shiva is a good boy"}}
