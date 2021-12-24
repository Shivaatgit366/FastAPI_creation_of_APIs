from fastapi import FastAPI
import fastapi_tutorials
from fastapi_tutorials.database import engine
import uvicorn
from fastapi_tutorials.routers import blog2
from fastapi_tutorials.routers import customers2
from routers import authentication2


"""
JWT - Jason Web Tokens will have expiration period and it is coded in a long string without any spaces.
Install python-jose to generate and verify the JWT tokens in Python.
Use the "create_access_token" function given in FastAPI documentation. Create the same function.
Use the "create_access_token" function to create the JWT token.
It is a function which returns jwt token for the given data.

Use the two schema/pydantic classes given in the FastAPI tutorial. Paste them inside the schemas.py file.
These classes should be sent as request body, these classes are helpful in verification of the user who has token.

In this example, it is used inside the "authentication2.py" file.
If the username and password are matched, then the function creates the JWT token.
"""


app = FastAPI()


fastapi_tutorials.database.Base.metadata.create_all(bind=engine)


app.include_router(blog2.router)
app.include_router(customers2.router)
app.include_router(authentication2.router)

if __name__ == '__main__':
    uvicorn.run("19th_part_JWT_token:app", reload=True)
