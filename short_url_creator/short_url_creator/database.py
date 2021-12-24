from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import urllib.parse

username = os.getenv("MYSQL_DB_USERNAME")
password = os.getenv("MYSQL_DB_PASSWORD")
host = os.getenv("MYSQL_DB_HOST")
database_name = os.getenv("MYSQL_DB_NAME")

quoted_password = urllib.parse.quote_plus(password)

SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://{username}:{quoted_password}@{host}/{database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
