from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi_tutorials import schema
from typing import List
from fastapi_tutorials.database import get_db
from fastapi_tutorials.o_auth2 import get_current_user
from fastapi_tutorials.repository import blog


router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request_body: schema.My_blog, db: Session = Depends(get_db),
           current_user: schema.Create_user = Depends(get_current_user)):
    # just return the function, it will take care of the rest.
    return blog.update_blog(id, request_body, db)


@router.get("", response_model=List[schema.Show_blog])
def all_blogs_returner(db: Session = Depends(get_db), current_user: schema.Create_user = Depends(get_current_user)):
    # we can simply call the function which is defined in other file.
    # By this way, codes can be kept neat and clean.
    return blog.get_all_blogs(db)


@router.post("", status_code=status.HTTP_201_CREATED)
def create(req_body: schema.My_blog, db: Session = Depends(get_db),
           current_user: schema.Create_user = Depends(get_current_user)):
    return blog.create_blog(req_body, db)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
# if 204 is given, then there will be no response body.
def destroy(id, db: Session = Depends(get_db), current_user: schema.Create_user = Depends(get_current_user)):
    return blog.delete_blog(id, db)


@router.get("/{id}", status_code=200, response_model=schema.Show_blog)
def id_row_returner(id: int, db: Session = Depends(get_db),
                    current_user: schema.Create_user = Depends(get_current_user)):
    return blog.get_blog_with_id(id, db)

