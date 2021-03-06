from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from fastapi_tutorials import schema
from fastapi_tutorials.database import get_db
from fastapi_tutorials import models
from fastapi_tutorials import hashing
from fastapi_tutorials import token_helper
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentication"])  # add the tag during the creation of "router" object.


@router.post("/login", response_model=schema.Token, status_code=status.HTTP_200_OK)
def login(request_body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # above step is given in FastAPI documentation.  request_body: OAuth2PasswordRequestForm = Depends()
    # This function provides the access token.
    # If the username and password are matched, then it returns the access token.
    user = db.query(models.Customer).filter(models.Customer.email == request_body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Invalid Email")
    if not hashing.verify_password(request_body.password, user.password):
        # remember: request_body.password is plain password, user.password is already hashed password.
        # If we give the arguments in reverse order, we get error.
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Invalid password")

    # if both the above conditions are satisfied, then provide the JWT token.
    access_token_expires = timedelta(minutes=token_helper.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token_helper.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


