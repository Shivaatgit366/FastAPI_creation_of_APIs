import token
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi_tutorials.schema import TokenData
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# "login" is the url/endpoint/path/route which creates the token. So, it is the tokenUrl.


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # this function returns the "coded JWT token" for any input data.
    # we provide email of the user as the data.
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# the below method is taken from "get_current_user" function from FastAPI documentation.
def verify_token(token: str, credentials_exception):
    # this function takes token as the input and another variable "credentials_exception"/error message as the input.
    # returns the error messages and verifies the token and returns token data.
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

