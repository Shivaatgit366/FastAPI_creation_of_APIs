from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from .. import models
from ..database import get_db
from .. import schema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # an object is created using "cryptcontext" class.


def create_customer(request_body: schema.Create_user, db: Session = Depends(get_db)):
    hashedPassword = pwd_context.hash(request_body.password)
    new_row = models.Customer(name=request_body.name, email=request_body.email, password=hashedPassword)
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row


def get_customer_with_id(id: int, db: Session = Depends(get_db)):
    record = db.query(models.Customer).filter(models.Customer.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
    else:
        return record
