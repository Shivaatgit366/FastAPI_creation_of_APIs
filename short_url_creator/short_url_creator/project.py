from datetime import datetime, timedelta
import uvicorn
from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from short_url_creator import schemas, models, database
from short_url_creator.database import SessionLocal, engine
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception


@app.get("/", tags=["short_url"])
def welcome():
    return "WELCOME TO URL SHORTENER"


@app.post("/sign_up", status_code=status.HTTP_201_CREATED, tags=["short_url"])
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    # using the "User" class, new object called "new_user" is created.
    # All the attributes of "User" class are updated in the "new_user" object.
    hashedPassword = pwd_context.hash(user.password)
    new_user = models.User(email=user.email, password=hashedPassword)
    db.add(new_user)  # add function adds the new object/record into the database.
    db.commit()
    db.refresh(new_user)
    print("Sign up successful, please enter the original url to be shortened")
    return new_user


@app.post("/login", status_code=status.HTTP_200_OK, tags=["short_url"])
def login_user(user_details: schemas.UserBase, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_details.email).first()
    # There is no need to hash the password, directly use "verify" method from pwd_context to verify the password.

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="your email is incorrect")
    else:
        if pwd_context.verify(user_details.password, existing_user.password):
            access_token = create_access_token(data={"sub": existing_user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            return "Wrong password, plz enter the correct password"


@app.post("/create_short_url", tags=["short_url"])
def create_url(url_details: schemas.ShorturlBase, db: Session = Depends(get_db)):
    url_object = models.Short_url(created_date=url_details.created_date,
                                  user_id=url_details.user_id,
                                  original_url=url_details.original_url)
    db.add(url_object)
    db.commit()
    db.refresh(url_object)
    return url_object


@app.post("/clicks", tags=["short_url"])
def click_count(clicks: schemas.Click, db: Session = Depends(get_db)):
    click_details = models.Click(date=clicks.date, short_url=clicks.short_url, click_count=clicks.click_count)
    db.add(click_details)
    db.commit()
    db.refresh(click_details)
    return click_details


if __name__ == '__main__':
    uvicorn.run("project:app", reload=True)

