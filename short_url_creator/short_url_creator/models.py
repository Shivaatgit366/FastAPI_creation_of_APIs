from short_url_creator.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, VARCHAR, Date


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(VARCHAR(250), unique=True, nullable=False)
    password = Column(VARCHAR(250), nullable=False)


class Short_url(Base):
    __tablename__ = "short_urls"

    created_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    original_url = Column(VARCHAR(1000), nullable=False)
    short_url = Column(VARCHAR(6), primary_key=True, nullable=False)


class Click(Base):
    __tablename__ = "clicks"

    date = Column(Date, primary_key=True, nullable=False)
    short_url = Column(VARCHAR(6), ForeignKey("short_urls.short_url"), primary_key=True, nullable=False)
    click_count = Column(Integer, nullable=False)
