from fastapi import FastAPI, Depends, status
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


@app.post("/blog", status_code=status.HTTP_201_CREATED)  # add a parameter "status_code" in the decorator method.
def create(req_body: schema.My_blog, db: Session = Depends(get_db)):  # status code can be found in documentation.
    new_blog = models.Blog(title=req_body.title, body=req_body.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
def all_blogs_returner(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}")
def id_row_returner(id, db: Session = Depends(get_db)):
    record = db.query(models.Blog).filter(models.Blog.id == id).all()
    return record


if __name__ == '__main__':
    uvicorn.run("6th_part_db:app", reload=True)
