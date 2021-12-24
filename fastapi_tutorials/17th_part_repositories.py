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

"""
Make a directory called "repository" and keep all the necessary files with functions in it.
Clean the blog.py and customers.py files. Just call the functions and they will take care of the rest.

Concept:- Further cleaning of path operating functions is possible.
We can keep the necessary codes in other files and reduce the content size.
"""

app = FastAPI()

fastapi_tutorials.database.Base.metadata.create_all(bind=engine)


app.include_router(blog2.router)
app.include_router(customers2.router)

if __name__ == '__main__':
    uvicorn.run("17th_part_repositories:app", reload=True)
