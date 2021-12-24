from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from fastapi_tutorials import models
from fastapi_tutorials.database import get_db
from fastapi_tutorials import schema


def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()  # .all() returns a list of objects.
    return blogs  # we get a list. List items will be the object attributes which will be in dictionary format.


def update_blog(id: int, request_body: schema.My_blog, db: Session = Depends(get_db)):
    row = db.query(models.Blog).filter(models.Blog.id == id)
    if not row.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your id {id} is not found")
    else:
        row.update(dict(request_body))
        db.commit()
        return {"message": f"your id {id} is updated"}


def create_blog(req_body: schema.My_blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req_body.title, body=req_body.body, user_id=2)  # user_id=1 is hard coded.
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete_blog(id: int, db: Session = Depends(get_db)):
    row = db.query(models.Blog).filter(models.Blog.id == id)
    if not row.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your id {id} is not found")
    else:
        row.delete(synchronize_session=False)
        db.commit()
        return {"message": f"the data at the id {id} has been deleted"}


def get_blog_with_id(id: int, db: Session = Depends(get_db)):
    record = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    return record

