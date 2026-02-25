import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from fastapi import Depends
# from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


username = os.environ.get("POSTGRES_SUPERUSER")
password = os.environ.get("POSTGRES_SUPERPW")
encoded_password = urllib.parse.quote_plus(str(password)) #Escaping Special Characters such as @ signs in Passwords
host = "localhost"
port="5432"
db = "inventory_db"

DATABASE_URL = f"postgresql://{username}:{encoded_password}@{host}/{db}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

