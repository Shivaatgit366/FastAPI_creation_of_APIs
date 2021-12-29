from fastapi import FastAPI
from typing import Optional, List
import uvicorn

app = FastAPI()


@app.get("/")
def welcome():
    return {"message": "Hello, Welcome to Blog Publisher"}


@app.post("/sign_in")
def sign_in():
    pass


@app.post("/sign_up")
def sign_up():
    pass


@app.get("/all_blogs_published_in_the_website_daywise")
def blogs_published_in_the_website_daywise():
    pass


@app.get("/about_the_author/{id}")
def author_details():
    pass


@app.get("/blogs_published_by_author_daywise")
def blogs_published_daywise():
    pass


@app.get("/blog/{id}")
def get_blog_with_id():
    pass


@app.put("/update_blog/{id}")
def update_blog():
    pass


@app.put("/update_author_info/{id}")
def update_author():
    pass


@app.delete("/delete_blog/{id}")
def delete_blog():
    pass


@app.delete("/delete_author/{id}")
def delete_author():
    pass


if __name__ == '__main__':
    uvicorn.run("project:app", reload=True)

