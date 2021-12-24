from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from fastapi_tutorials import schema
from fastapi_tutorials import models
from fastapi_tutorials.database import engine, SessionLocal
import uvicorn
from sqlalchemy.orm import Session
from passlib.context import CryptContext


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request_body: schema.My_blog, db: Session = Depends(get_db)):
    row = db.query(models.Blog).filter(models.Blog.id == id)
    if not row.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your id {id} is not found")
    else:
        # print(request_body.dict(exclude_unset=True))  # pydantic model documentation has model.dict method.
        # row.update(request_body.dict(exclude_unset=True))  # pydantic model doc has dict(model) method also.
        # by using dict(model), attributes of the model/object can be obtained in dictionary format.
        row.update(dict(request_body))
        db.commit()
        return {"message": f"your id {id} is updated"}


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(req_body: schema.My_blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req_body.title, body=req_body.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{id}", status_code=status.HTTP_200_OK)  # # if 204 is given, then there will be no response body.
def destroy(id, db: Session = Depends(get_db)):
    row = db.query(models.Blog).filter(models.Blog.id == id)
    if not row.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your id {id} is not found")
    else:
        row.delete(synchronize_session=False)
        db.commit()
        return {"message": f"the data at the id {id} has been deleted"}


"""
"passlib" library is used for password hashing. Recommended algorithm for password hashing is "bcrypt".
Import the crypt context from the passlib library.
First install the passlib and bcrypt     pip install "passlib[bcrypt]".
From passlib.context, we should import CryptContext.
Finally, an object called pwd_context will be created using the class "CryptContext" with few hashing attributes.
"""


@app.get("/blog", response_model=List[schema.Show_blog])  # response model is added, desired response can be obtained.
def all_blogs_returner(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()  # .all() returns a list of objects.
    return blogs  # we get a list of objects and each object in the list is a dictionary.


# response_model = desired model/class what we have created in the schema.py. It is also a pydantic model.
# add it in the decorator.
@app.get("/blog/{id}", status_code=200, response_model=schema.Show_blog)
def id_row_returner(id, response: Response, db: Session = Depends(get_db)):
    record = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not record:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error_message": f"your id {id} is not found"}
    return record


# this pwd_context object has an attribute called "hash" function which encrypts the user entered password.
# Encrypted password is stored inside the variable.
# Instead of schema password, hashed password will be sent in the post request.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # an object is created using "cryptcontext" class.


@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(request_body: schema.Create_user, db: Session = Depends(get_db)):
    hashedPassword = pwd_context.hash(request_body.password)
    new_row = models.Customer(name=request_body.name, email=request_body.email, password=hashedPassword)
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row


if __name__ == '__main__':
    uvicorn.run("11th_part_password_hash:app", reload=True)
