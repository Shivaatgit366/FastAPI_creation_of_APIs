from fastapi import FastAPI, Depends
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


# 2 types of models are used as parameters.
# Pydantic model(for data validation) and SQLalchemy model(the class made in model.py file).
@app.post("/blog")
def create(req_body: schema.My_blog, db: Session = Depends(get_db)):  # db gets converted into pydantic type.
    new_blog = models.Blog(title=req_body.title, body=req_body.body)  # class Blog from Models is used for instance.
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
def all_blogs_returner(db: Session = Depends(get_db)):  # database is required as a parameter to do query.
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}")
def id_row_returner(id, db: Session = Depends(get_db)):
    record = db.query(models.Blog).filter(models.Blog.id == id).all()
    return record


if __name__ == '__main__':
    uvicorn.run("5th_part_db_connection:app", reload=True)
