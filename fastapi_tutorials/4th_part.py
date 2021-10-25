from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):  # "Blog" is the model we created, this model contains the contents for the request body.
    title: str
    description: Optional[str] = None
    body: str
    published: Optional[bool] = None
    pass


@app.post("/shiva")
def create_blog(make_blog_request: Blog):  # make_blog_request is the parameter, it is of the datatype "Blog model".
    return {"data": "blog is created"}  # return means "response". In this case, request body is empty.


@app.post("/blog")
def create_blog(blog_request: Blog):
    return {"data": f"blog is created with the title as {blog_request.title}"}


@app.get("/blog")
def index(published: bool = True, limit=10, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} blogs from the database are displayed, the value of published is {published}"}
    else:
        return {"data": f"{limit} blogs are displayed only"}


@app.get("/about")
def about():
    return {"data": {"about page": "shiva is a good boy"}}


@app.get("/blog/unpublished_items")
def unpublished():
    return {"data": "unpublished items will be displayed in this page"}


@app.get("/blog/{blog_id}")
def blog(blog_id: int):
    return {"data": blog_id}


@app.get("/blog/{blog_id}/comments")
def comments(blog_id, limit=10):
    return {"data": {blog_id: "people gave good comments about the api", "values": {1, 2}, "limit": {limit}}}
