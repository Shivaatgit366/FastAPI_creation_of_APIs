from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from fastapi_tutorials import schema
from fastapi_tutorials.database import get_db
from fastapi_tutorials import models
from fastapi_tutorials import hashing


router = APIRouter(tags=["Authentication"])  # add the tag during the creation of "router" object.


@router.post("/login", status_code=status.HTTP_200_OK)
def login(request_body: schema.Login, db: Session = Depends(get_db)):  # In this example, username means email.
    user = db.query(models.Customer).filter(models.Customer.email == request_body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Invalid Email")
    if not hashing.verify_password(request_body.password, user.password):
        # remember: request_body.password is plain password, user.password is already hashed password.
        # If we give the arguments in reverse order, we get error.
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Invalid password")
    # if both the above conditions are satisfied, then provide the JWT token.
    else:
        return user

