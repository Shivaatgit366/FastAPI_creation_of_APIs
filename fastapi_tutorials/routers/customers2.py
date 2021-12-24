from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi_tutorials import schema
from fastapi_tutorials.database import get_db
from fastapi_tutorials.repository import customers
from fastapi_tutorials.o_auth2 import get_current_user


router = APIRouter(prefix="/user", tags=["Customers"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schema.Show_user)
def create_user(request_body: schema.Create_user, db: Session = Depends(get_db),
                current_user: schema.Create_user = Depends(get_current_user)):
    return customers.create_customer(request_body, db)


@router.get("/{id}", status_code=200, response_model=schema.Show_user)
def user_id_returner(id: int, db: Session = Depends(get_db),
                     current_user: schema.Create_user = Depends(get_current_user)):
    return customers.get_customer_with_id(id, db)
