from fastapi import FastAPI
import fastapi_tutorials
from fastapi_tutorials.database import engine
import uvicorn
from fastapi_tutorials.routers import blog2
from fastapi_tutorials.routers import customers2
from routers import authentication2


"""
In this file we try to put all the routes behind the authentication. Paths will open only if it's authenticated.
From FastAPI documentation, use the "get_current_user" function.
The function takes "token" as the input and checks whether the user is current user or not.
This function uses dependency function to check whether the token is valid or not.
If the token is matched and valid without expiration, then he is the current user.


To put route behind authentication, just add "get_current_user" function as an argument in the path operating function.
We get the lock symbol in the swagger UI.
See the codes @ /routers.blog2.py file.
"""


app = FastAPI()


fastapi_tutorials.database.Base.metadata.create_all(bind=engine)


app.include_router(blog2.router)
app.include_router(customers2.router)
app.include_router(authentication2.router)

if __name__ == '__main__':
    uvicorn.run("20th_part_behind_authentication:app", reload=True)

