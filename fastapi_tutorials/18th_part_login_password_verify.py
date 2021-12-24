from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
import fastapi_tutorials
from fastapi_tutorials import schema
from fastapi_tutorials import models
from fastapi_tutorials.database import engine, SessionLocal, get_db
import uvicorn
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi_tutorials.routers import blog2
from fastapi_tutorials.routers import customers2
from routers import authentication


"""
An endpoint/route/path for "login" is created using APIRouter.
Create a "login" class in schema.py for the post request by users.
Now, check for the username/email and password by using sql alchemy queries.
If both username and password gets matched, then return a JWT token which will have a validity period.
"""


app = FastAPI()

fastapi_tutorials.database.Base.metadata.create_all(bind=engine)


app.include_router(blog2.router)
app.include_router(customers2.router)
app.include_router(authentication.router)

if __name__ == '__main__':
    uvicorn.run("18th_part_login_password_verify:app", reload=True)

