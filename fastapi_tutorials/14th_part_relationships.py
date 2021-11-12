from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
from pydantic import BaseModel

import fastapi_tutorials
from fastapi_tutorials import schema
from fastapi_tutorials import models
from fastapi_tutorials.database import engine, SessionLocal
import uvicorn
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()

fastapi_tutorials.database.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
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


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(req_body: schema.My_blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req_body.title, body=req_body.body, user_id=2)  # user_id=1 is hard coded.
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{id}", status_code=status.HTTP_200_OK, tags=["Blogs"])
# if 204 is given, then there will be no response body.
def destroy(id, db: Session = Depends(get_db)):
    row = db.query(models.Blog).filter(models.Blog.id == id)
    if not row.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your id {id} is not found")
    else:
        row.delete(synchronize_session=False)
        db.commit()
        return {"message": f"the data at the id {id} has been deleted"}


"""
A table can have only ONE primary key; The primary key can consist of single or multiple columns (fields).
The FOREIGN KEY constraint is used to prevent actions that would destroy relationship between tables.

A FOREIGN KEY is a field (or collection of fields) in one table, that refers to the PRIMARY KEY in another table.
The table with the foreign key is called the child table. The table with the primary key is called the parent table.

Here is an example:-
The "PersonID" column in the "Persons" table is the PRIMARY KEY in the "Persons" table.
The "PersonID" column in the "Orders" table is a FOREIGN KEY in the "Orders" table.

concept:-
First import relationship from sqlalchemy.orm in model.py file.
Define the Foreign key, mention it in the required code.
Use relationship() function, mention the name of the class and back populate with the attribute of that class.

To get desired response, we must create response model in schema.py file.
Add the attributes of the classes we created using relationship().
Then mention the type of the attributes as the another table's response model.
Foreign key will be matched and we get the suitable rows from the different tables.
We get the response in the form of nested dictionary.
"""


@app.get("/blog", response_model=List[schema.Show_blog], tags=["Blogs"])
# response model is added, desired response can be obtained.
def all_blogs_returner(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()  # .all() returns a list of objects.
    return blogs  # we get a list of objects and each object in the list is a dictionary.


# response_model = desired model/class what we have created in the schema.py. It is also a pydantic model.
# add it in the decorator.
@app.get("/blog/{id}", status_code=200, response_model=schema.Show_blog, tags=["Blogs"])
def id_row_returner(id: int, response: Response, db: Session = Depends(get_db)):
    record = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not record:
        # the below code does not work. Do not use it. Use "raise HTTPException" statement for raising the error.
        # response.status_code = status.HTTP_200_OK
        # return {"error_message": f"your id {id} is not found"}

        # below is the correct method to get the desired error message.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    return record


# this pwd_context object has an attribute called "hash function" which encrypts the user entered password.
# Encrypted password is stored inside the variable, it will be sent as the post request instead of the real password.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # an object is created using "cryptcontext" class.


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schema.Show_user, tags=["Customers"])
# response model is added.
def create_user(request_body: schema.Create_user, db: Session = Depends(get_db)):
    hashedPassword = pwd_context.hash(request_body.password)
    new_row = models.Customer(name=request_body.name, email=request_body.email, password=hashedPassword)
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row


@app.get("/user/{id}", status_code=200, response_model=schema.Show_user, tags=["Customers"])
def user_id_returner(id, response: Response, db: Session = Depends(get_db)):
    record = db.query(models.Customer).filter(models.Customer.id == id).first()
    if not record:
        # the below code does not work. Do not use it. Use "raise HTTPException" statement for raising the error.
        # response.status_code = status.HTTP_200_OK
        # return {"error_message": f"your id {id} is not found"}

        # below is the correct method to get the desired error message.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
    else:
        return record


if __name__ == '__main__':
    uvicorn.run("14th_part_relationships:app", reload=True)

