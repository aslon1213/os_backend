from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session
from config import config

MYSQL_URL = config.MYSQL_URL
SQLITE_URL = config.SQLITE_URL


print("INITIALIZING DATABASE")
engine = create_engine(SQLITE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
import os


def get_db():
    try:
        db = sessionLocal()
    except:
        os._exit(1)
    return db
