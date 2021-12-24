from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_tutorials import token_helper


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# "login" is the url/endpoint/path/route which creates the token. So, it is the tokenUrl.


# below function is taken from "get_current_user" function from FastAPI documentation.
# In our project, we only check whether the token is expired or not.
# In the FastAPI documentation, he detects the user who has taken the token also.
def get_current_user(token: str = Depends(oauth2_scheme)):
    # takes "token" as input, checks whether the user is current user or not.
    # returns token data also.
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return token_helper.verify_token(token, credentials_exception)
