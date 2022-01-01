from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import urllib.parse

# print(os.environ)  # gives all the environment variables and their values in the dictionary format.

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
db_name = os.getenv("MYSQL_DB_NAME")
mysql_server = os.getenv("MYSQL_HOST")

quoted_password = urllib.parse.quote_plus(password)

SQLALCHEMY_DATABASE_URL = f"mysql://{user}:{quoted_password}@{mysql_server}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

