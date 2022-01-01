from sqlalchemy import Column, ForeignKey, Integer, String, Date, VARCHAR
from blog_publisher.database import Base


class Authors(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(VARCHAR(250), unique=True, nullable=False)
    password = Column(VARCHAR(250), nullable=False)


class Blogs(Base):
    __tablename__ = "blogs"

    blog_id = Column(VARCHAR(6), primary_key=True, nullable=False)
    published_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.author_id"), nullable=False)
    title = Column(VARCHAR(1000), nullable=False)
    body = Column(String(4294000000), nullable=False)

