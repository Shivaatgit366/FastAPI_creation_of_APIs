# from typing import Optional
# from fastapi import FastAPI
#
# app = FastAPI()
#
# # query parameter starts with "?" symbol and has key=value pairs with the symbol "&" in between the pairs.
# # Path parameter means variable used in the path/url. We should accept both path and query parameters in the function.
#
#
# @app.get("/blog")  # Remember:- Only in the browser, we should add query parameter for the path/url.
# def index(published: bool = True, limit=10, sort: Optional[str] = None):
#     # keys in query parameter should be accepted as the argument for the function.
#     # if the default values are set for the keys, then those keys can be removed in the query parameter.
#
#     if published:
#         return {"data": f"{limit} blogs from the database are displayed, the value of published is {published}"}
#     else:
#         return {"data": f"{limit} blogs are displayed only"}
#
#
# @app.get("/about")
# def about():
#     return {"data": {"about page": "shiva is a good boy"}}
#
#
# @app.get("/blog/unpublished_items")
# def unpublished():
#     return {"data": "unpublished items will be displayed in this page"}
#
#
# @app.get("/blog/{blog_id}")
# def blog(blog_id: int):
#     return {"data": blog_id}
#
#
# @app.get("/blog/{blog_id}/comments")  # path parameter and query parameter both can exist in a function.
# def comments(blog_id, limit=10): # query parameter is set to 10, we can delete that key in query parameter in browser.
#     return {"data": {blog_id: "people gave good comments about the api", "values": {1, 2}, "limit": {limit}}}
# -------------------------------------------------------------------------------------------------------------
