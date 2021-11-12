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
An example of "File structure for bigger applications/multiple files" is given in FastAPI documentation".
"router" object is created using APIRouter().
Then we can create all the endpoints/paths using the same old decorator method.
But, this time, there is no need to keep the endpoints/functions in the "main.py" file.
We can keep the "main.py" file neat and clean.

Create the desired endpoints using "router" object in the "blog.py", "customers.py" files.
These files are kept inside the "routers" folder.
Then import "blog.py" and "customers.py" files into the "main.py" file.
Include the "router" objects with the "app" object in the "main.py" file.
Run the "main.py" file and we get all the endpoints as it was used to be earlier.
By this technique, we can keep the "main.py" file neat and clean. Also we get all the required endpoints.
"""

app = FastAPI()

fastapi_tutorials.database.Base.metadata.create_all(bind=engine)

# "router" object in "blog.py" file is added with "app" object present in "main.py" file.
# "router" object in "customers.py" file is added with "app" object present in "main.py" file.
app.include_router(blog.router)
app.include_router(customers.router)

if __name__ == '__main__':
    uvicorn.run("15th_part_API_Router:app", reload=True)
