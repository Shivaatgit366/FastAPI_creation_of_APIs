from fastapi import APIRouter, Depends, status, HTTPException, Response
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi_tutorials import schema
from typing import List
from fastapi_tutorials import models
from fastapi_tutorials.database import get_db

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # an object is created using "cryptcontext" class.


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schema.Show_user, tags=["Customers"])
# response model is added.
def create_user(request_body: schema.Create_user, db: Session = Depends(get_db)):
    hashedPassword = pwd_context.hash(request_body.password)
    new_row = models.Customer(name=request_body.name, email=request_body.email, password=hashedPassword)
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row


@router.get("/user/{id}", status_code=200, response_model=schema.Show_user, tags=["Customers"])
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
