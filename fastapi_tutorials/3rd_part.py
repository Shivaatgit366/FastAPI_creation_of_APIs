# from typing import Optional
# from fastapi import FastAPI

# app = FastAPI()

# concept:- A request body is data sent by the client/browser to your API.
# A response body is the data your API sends to the client/browser.
# To send data, we should use one of: POST (the more common), PUT, DELETE or PATCH.
# If the data is sent through GET request, it will create an undefined behavior in the specifications.
# Sending the request body/data through GET request is done only in exceptional cases.


# Remember:- Post methods need "models as parameter" for the path operating function.
# We can't send/access the post method through browser. Use SwaggerUI to check the API.
# Only the model(class made by pydantic library) can be used as the parameter for the path operating function.


# @app.post("/shiva")
# def create_blog():  # no parameters are given for this function.
#     return {"data": "blog is created"}


# @app.get("/blog")
# def index(published: bool = True, limit=10, sort: Optional[str] = None):

    # if published:
    #     return {"data": f"{limit} blogs from the database are displayed, the value of published is {published}"}
    # else:
    #     return {"data": f"{limit} blogs are displayed only"}


# @app.get("/about")
# def about():
#     return {"data": {"about page": "shiva is a good boy"}}


# @app.get("/blog/unpublished_items")
# def unpublished():
#     return {"data": "unpublished items will be displayed in this page"}


# @app.get("/blog/{blog_id}")
# def blog(blog_id: int):
#     return {"data": blog_id}


# @app.get("/blog/{blog_id}/comments")
# def comments(blog_id, limit=10):
#     return {"data": {blog_id: "people gave good comments about the api", "values": {1, 2}, "limit": {limit}}}
# --------------------------------------------------------------------------------------------------------------
