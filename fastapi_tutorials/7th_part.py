from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi_tutorials import schema
from fastapi_tutorials import models
from fastapi_tutorials.database import engine, SessionLocal
import uvicorn
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(req_body: schema.My_blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req_body.title, body=req_body.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
def all_blogs_returner(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# to create custom status_code, import "Response" from FastAPI. Add that type of parameter in the path function.
@app.get("/blog/{id}", status_code=200)
def id_row_returner(id, response: Response, db: Session = Depends(get_db)):
    record = db.query(models.Blog).filter(models.Blog.id == id).first()
    # record is an object which has the details of a row. If "id" doesn't exist, then record also will not exist.
    # attributes of the object "record" is shown in JSON format in the response. It is done by FastAPI.
    # response looks like    {"title": "bb blog", "body": "hello hello", "id": 6}
    if not record:  # if the record does not exist, then below condition can be used.
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error_message": f"your id {id} is not found"}
    print(record.id, record.title, record.body)
    return record


# Instead of the use of custom error message, we can use standard method to raise HTTP error.
# to raise HTTPException, we can import HTTPException from FastAPI, then use "raise" keyword as shown below.
# If you do as per below method, then the parameter "response" is not required. No need to import "Response".


"""
@app.get("/blog/{id}", status_code=200)
def id_row_returner(id, db: Session = Depends(get_db)):
    record = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your id {id} is not found")
    return record
"""


if __name__ == '__main__':
    uvicorn.run("7th_part:app", reload=True)
