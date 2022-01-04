from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, List
import uvicorn, random, string
from blog_publisher import schemas, database, models
from blog_publisher.database import SessionLocal, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sign_in")


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
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find the credentials")
        current_user = db.query(models.Authors).filter(models.Authors.email == email).first()
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not find the credentials")
        return current_user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token is expired")


@app.get("/", tags=["blog publisher"])
def welcome():
    return {"message": "Welcome to Blog Publisher"}


@app.post("/sign_up", status_code=status.HTTP_201_CREATED, tags=["authors"])
def sign_up(request_body: schemas.AuthorBase, db: Session = Depends(get_db)):
    hashedPassword = pwd_context.hash(request_body.password)
    new_author = models.Authors(email=request_body.email, password=hashedPassword)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@app.post("/sign_in", status_code=status.HTTP_200_OK, tags=["authors"], response_model=schemas.Token)
def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_author = db.query(models.Authors).filter(models.Authors.email == form_data.username).first()
    if not existing_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your email not found")
    else:
        verify_password = pwd_context.verify(form_data.password, existing_author.password)
        if not verify_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password not matched")
        else:
            access_token = create_access_token(data={"sub": existing_author.email})
            return {"access_token": access_token, "token_type": "bearer"}


@app.post("/blogs", status_code=status.HTTP_201_CREATED, response_model=schemas.Blog, tags=["blogs"], )
def create_new_blog(req_blog: schemas.BlogCreate, db: Session = Depends(get_db),
                    current_author: models.Authors = Depends(get_current_user)):
    today = datetime.now().date()
    blog_id = generate_random_string(length=6)
    existing_author = db.query(models.Authors).filter(models.Authors.email == current_author.email).first()
    id = existing_author.author_id
    new_blog = models.Blogs(blog_id=blog_id, created_date=today,
                            author_id=id, title=req_blog.title, body=req_blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.post("/blogs/{blog_id}/publish", tags=["blogs"], response_model=schemas.Blog)
def publish_your_blog(blog_id: str, db: Session = Depends(get_db),
                      current_author: models.Authors = Depends(get_current_user)):
    publish_day = datetime.now().date()
    existing_blog = db.query(models.Blogs).filter(models.Blogs.blog_id == blog_id,
                                                  models.Blogs.author_id == current_author.author_id).first()
    if not existing_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with the id {blog_id} is not found")
    # we can simply use "db.add()" function in sqlalchemy, it will update the given columns.
    # another way of updating the table is to use "update" method.
    if existing_blog.status != models.StatusTypes.PUBLISHED:
        existing_blog.status = models.StatusTypes.PUBLISHED
        existing_blog.published_date = publish_day
        db.add(existing_blog)
        db.commit()
        db.refresh(existing_blog)
    return existing_blog


@app.get("/blogs", status_code=status.HTTP_200_OK, response_model=List[schemas.BlogSummary], tags=["blogs"])
def get_all_blogs(db: Session = Depends(get_db), current_author: models.Authors = Depends(get_current_user)):
    blogs = db.query(models.Blogs).filter(models.Blogs.author_id == current_author.author_id).all()
    return blogs


@app.get("/blogs/{blog_id}", response_model=schemas.Blog, tags=["blogs"])
def get_one_blog(blog_id: str, db: Session = Depends(get_db),
                 current_author: models.Authors = Depends(get_current_user)):
    existing_blog = db.query(models.Blogs).filter(models.Blogs.blog_id == blog_id,
                                                  models.Blogs.author_id == current_author.author_id).first()
    if not existing_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog id is incorrect")
    return existing_blog


@app.patch("/blogs/{blog_id}", tags=["blogs"], response_model=schemas.Blog)
def update_blog(blog_id: str, req_body: schemas.BlogUpdate, db: Session = Depends(get_db),
                current_author: models.Authors = Depends(get_current_user)):
    existing_blog = db.query(models.Blogs).filter(models.Blogs.blog_id == blog_id,
                                                  models.Blogs.author_id == current_author.author_id).first()
    if not existing_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog id is incorrect")

    if existing_blog.status == models.StatusTypes.PUBLISHED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="published blog can not be edited")

    else:
        update_dict = req_body.dict(exclude_unset=True)
        # "req_body" is an object from pydantic model.
        # ".dict" function gives the dictionary made from the attributes of the object.
        if update_dict:
            if "title" in update_dict and update_dict["title"] is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title can not be null")
            elif "body" in update_dict and update_dict["body"] is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Body can not be null")
            else:
                db.query(models.Blogs).filter(models.Blogs.blog_id == blog_id).update(update_dict,
                                                                                      synchronize_session=False)
                db.commit()
        return existing_blog

    # else:
    # we can update in 2 ways. By using "db.add()" function just like below.
    #     existing_blog.title = req_body.title
    #     existing_blog.body = req_body.body
    #     db.add(existing_blog)
    #     db.commit()

    # we can update by "update()" function by creating the required dictionary. Select the object and update as below.
    #     # response_dict = {"title": req_body.title, "body": req_body.body}
    #     # db.query(models.Blogs).filter(models.Blogs.blog_id == blog_id).update(response_dict,
    #                                                                             synchronize_session=False)
    #     db.commit()
    #     return existing_blog


@app.delete("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete_blog(blog_id: str, db: Session = Depends(get_db),
                current_author: models.Authors = Depends(get_current_user)):
    existing_blog = db.query(models.Blogs).filter(models.Blogs.blog_id == blog_id,
                                                  models.Blogs.author_id == current_author.author_id).first()
    if not existing_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog id is incorrect")
    else:
        db.query(models.Blogs).filter(models.Blogs.blog_id == blog_id).delete(synchronize_session=False)
        db.commit()


if __name__ == '__main__':
    uvicorn.run("project:app", reload=True)

