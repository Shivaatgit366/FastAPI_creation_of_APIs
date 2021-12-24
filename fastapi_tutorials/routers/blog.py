from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi_tutorials import schema
from typing import List
from fastapi_tutorials import models
from fastapi_tutorials.database import get_db

router = APIRouter(prefix="/blog", tags=["Blogs"])
# during the object initiation itself we can include tags, prefixes, responses and dependencies.
# Just like "app" is created using FastAPI(), "router" object is created using APIRouter().


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request_body: schema.My_blog, db: Session = Depends(get_db)):
    row = db.query(models.Blog).filter(models.Blog.id == id)
    if not row.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your id {id} is not found")
    else:
        row.update(dict(request_body))
        db.commit()
        return {"message": f"your id {id} is updated"}


@router.get("", response_model=List[schema.Show_blog])
def all_blogs_returner(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()  # .all() returns a list of objects.
    return blogs  # we get a list. List items will be the object attributes which will be in dictionary format.


@router.post("", status_code=status.HTTP_201_CREATED)
def create(req_body: schema.My_blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req_body.title, body=req_body.body, user_id=2)  # user_id=1 is hard coded.
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{id}", status_code=status.HTTP_200_OK)
# if 204 is given, then there will be no response body.
def destroy(id, db: Session = Depends(get_db)):
    row = db.query(models.Blog).filter(models.Blog.id == id)
    if not row.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your id {id} is not found")
    else:
        row.delete(synchronize_session=False)
        db.commit()
        return {"message": f"the data at the id {id} has been deleted"}


@router.get("/{id}", status_code=200, response_model=schema.Show_blog)
def id_row_returner(id: int, response: Response, db: Session = Depends(get_db)):
    record = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not record:
        # the below code does not work. Do not use it. Use "raise HTTPException" statement for raising the error.
        # response.status_code = status.HTTP_200_OK
        # return {"error_message": f"your id {id} is not found"}

        # below is the correct method to get the desired error message.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    return record
