from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
import fastapi_tutorials
from fastapi_tutorials import schema
from fastapi_tutorials import models
from fastapi_tutorials.database import engine, SessionLocal, get_db
import uvicorn
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi_tutorials.routers import blog
from fastapi_tutorials.routers import customers

"""
While defining the object itself we can add prefixes, tags, responses, dependencies which are repeated everywhere.
These repetitive things can be unwritten during the code.
"""

app = FastAPI()

fastapi_tutorials.database.Base.metadata.create_all(bind=engine)


app.include_router(blog.router)
app.include_router(customers.router)

if __name__ == '__main__':
    uvicorn.run("16th_part_API_Router_Path_Operators:app", reload=True)
