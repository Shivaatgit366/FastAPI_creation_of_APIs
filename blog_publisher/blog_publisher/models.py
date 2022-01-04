from sqlalchemy import Column, ForeignKey, Integer, String, Date, VARCHAR, Enum
from blog_publisher.database import Base
import enum


class StatusTypes(enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"


class Authors(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(VARCHAR(250), unique=True, nullable=False)
    password = Column(VARCHAR(250), nullable=False)


class Blogs(Base):
    __tablename__ = "blogs"

    blog_id = Column(VARCHAR(6), primary_key=True, nullable=False)
    created_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.author_id"), nullable=False)
    title = Column(VARCHAR(1000), nullable=False)
    body = Column(String(4294000000), nullable=False)
    published_date = Column(Date, nullable=True)  # "nullable=True" should be specified. "Null" is the default value.
    status = Column(Enum(StatusTypes), default=StatusTypes.DRAFT.value, nullable=False)

