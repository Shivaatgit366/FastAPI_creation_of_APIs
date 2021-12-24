from fastapi import FastAPI

app = FastAPI()  # object is created by calling the FastAPI class.

# get, post, put, delete are called operators in FastAPI. They do operation on the endpoint/path.
# functions which helps to do path operation is called "path operation function".
# add the file "__init__.py" inside any directory to make that directory a python "module".


@app.get("/")  # "/" means base url, original server url. Path or the endpoint is local host itself.
def index():  # function name can be anything, only path/endpoint matters.
    return {"data": "blog list"}


@app.get("/about")  # get function takes the endpoint/path/route as an argument.
def about():  # only the path matters.
    return {"data": {"about page": "shiva is a good boy"}}


@app.get("/blog/unpublished_items")
def unpublished():
    return {"data": "unpublished items will be displayed in this page"}


@app.get("/blog/{blog_id}")  # use curly brackets to add any variable in the path. Variable can have different values.
def blog(blog_id: int):  # function takes that variable as the argument. Mention the variable type in the function.
    # by default, browser takes the variable as a string. It is very important to specify the variable type.
    # fetch the blog id with variable "blog_id"
    return {"data": blog_id}  # string of the variable will be returned.


@app.get("/blog/{blog_id}/comments")
def comments(blog_id):
    return {"data": {blog_id: "people gave good comments about the api", "values": {1, 2}}}


# In FastAPI we can check the created API through automatic docs which is given by SwaggerUI.
# Just go to "/docs" end point in the browser, we can see the status of the API by SwaggerUI.
# Just go to "/redoc" end point in the browser, we can see the status of the API by Redoc.
# ---------------------------------------------------------------------------------------------------------------

