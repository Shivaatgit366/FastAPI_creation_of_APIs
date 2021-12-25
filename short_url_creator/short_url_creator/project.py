from datetime import datetime, timedelta
import uvicorn, random, string, webbrowser
from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.responses import RedirectResponse
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from short_url_creator import schemas, models, database
from short_url_creator.database import SessionLocal, engine
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
           "http://localhost", "http://localhost:8080"]

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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


def generate_random_string(length=6):
    random_list = random.choices(string.ascii_lowercase + string.digits, k=length)
    return "".join(random_list)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user_object = db.query(models.User).filter(models.User.email == email).first()
        if user_object is not None:
            return user_object
        else:
            raise credentials_exception
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
    return new_user


@app.post("/login", status_code=status.HTTP_200_OK, tags=["short_url"])
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    # There is no need to hash the password, directly use "verify" method from pwd_context to verify the password.
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="your email is incorrect")
    else:
        if pwd_context.verify(form_data.password, existing_user.password):
            access_token = create_access_token(data={"sub": existing_user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            return "Wrong password, plz enter the correct password"


@app.post("/create_short_url", tags=["short_url"], response_model=schemas.Short_Url)
def create_url(url_details: schemas.ShorturlBase, db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):
    current_date = datetime.now().date()
    short_url = generate_random_string()
    url_object = models.Short_url(created_date=current_date,
                                  user_id=current_user.user_id,
                                  original_url=url_details.original_url,
                                  short_url=short_url)
    db.add(url_object)
    db.commit()
    db.refresh(url_object)
    return url_object


@app.get("/list_of_shorturls", response_model=List[schemas.Short_Url], tags=["short_url"])
def get_all_short_urls(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    list_of_urls = db.query(models.Short_url).filter(models.Short_url.user_id == current_user.user_id).all()
    return list_of_urls


@app.get("/daily_shorturls_created_by_user", status_code=status.HTTP_200_OK,
         response_model=List[schemas.ShortUrlCount], tags=["short_url"])
def daywise_urls_created_by_user(db: Session = Depends(get_db),
                                 current_user: models.User = Depends(get_current_user)):
    # aggregate function "count" is used here.
    # We can select "created date", "user id", "count(short url)" to use "group by" command.
    # When specific columns are selected from the table, we get list of tuples which has attributes of the object.
    daywise_counts = db.query(models.Short_url.created_date,
                              func.count(models.Short_url.short_url)). \
        filter(models.Short_url.user_id == current_user.user_id).all()
    result = []
    for created_date, count in daywise_counts:  # list with tuples.
        result.append({"created_date": created_date, "short_urls_count": count})
    return result


@app.get("/{short_url}", status_code=status.HTTP_202_ACCEPTED, tags=["short_url"])
def go_to_original_url(short_url: str, db: Session = Depends(get_db)):
    existing_url = db.query(models.Short_url).filter(models.Short_url.short_url == short_url).first()
    if not existing_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid url")

    today = datetime.now().date()  # returns date
    click_count_obj = db.query(models.Click).filter(models.Click.date == today,
                                                    models.Click.short_url == existing_url.short_url).first()
    if click_count_obj:
        click_count_obj.click_count = click_count_obj.click_count + 1
        db.add(click_count_obj)
        db.commit()
        db.refresh(click_count_obj)
    else:
        # content will be added to the "clicks" table.
        click_count_obj = models.Click(date=today, short_url=existing_url.short_url, click_count=1)
        db.add(click_count_obj)
        db.commit()
        db.refresh(click_count_obj)
    return RedirectResponse(url=existing_url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/daily_click_counts/{short_url}", status_code=status.HTTP_200_OK,
         tags=["short_url"], response_model=List[schemas.Clicks])
def daywise_click_counts(short_url: str, db: Session = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)):
    existing_short_url = db.query(models.Short_url).filter(
        models.Short_url.short_url == short_url,
        models.Short_url.user_id == current_user.user_id).first()
    if not existing_short_url:
        raise HTTPException(status_code=404, detail="You have not created such url")

    # 2 conditions can be written as below.
    # existing_short_url = db.query(models.Short_url).filter(models.Short_url.short_url == short_url).first()
    # if not existing_short_url:
    #     raise HTTPException(status_code=404)
    # if existing_short_url.user_id != current_user.user_id:
    #     raise HTTPException(status_code=403, detail="permission denied")

    click_counts = db.query(models.Click).filter(models.Click.short_url == short_url).order_by(
        models.Click.date.asc()).all()
    return click_counts


if __name__ == '__main__':
    uvicorn.run("project:app", reload=True)
