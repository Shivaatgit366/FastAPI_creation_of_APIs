from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi_tutorials import database


class Blog(database.Base):
    # here, we are creating a table inside the db. Attributes of class are the fields of that table.
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("customers.id"))

    user = relationship("Customer", back_populates="blog")


class Customer(database.Base):
    # attributes of model/class are the fields of the table. This step creates another table in db.
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blog = relationship("Blog", back_populates="user")
