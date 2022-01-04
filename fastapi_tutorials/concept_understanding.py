from pydantic import BaseModel
from typing import Optional


# These dict methods are only for the pydantic library in python.
class BlogUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


# we have a pydantic model/class above. A new object will be created using the above class.

shiva_obj = BlogUpdate()  # an object is created using pydantic model/class.

print(f"name of the object is {shiva_obj}")  # we get something without commas or any datatype.
# It means it is an object.

print(f"dict(object) will give {dict(shiva_obj)}")  # object attributes are converted into the dictionary.

print(f"object.dict() will give the result {shiva_obj.dict()}")
# same as above example, object attributes are converted into the dictionary.

print(f"during object creation, exclude the unset keys."
      f" If all the attributes are set to None, then also no problem. We get values as None."
      f" If we don't set any values, then we get {shiva_obj.dict(exclude_unset=True)}")
# so we get only the empty dictionary because we have not set any keys.

