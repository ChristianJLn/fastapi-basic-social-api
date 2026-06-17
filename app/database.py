from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# import uuid
# import time

# Holi mi amor

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

""" while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi-basic-social-db",
                                user="postgres", password="jfSAi8445bi2")
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as e:
        print("Connecting to database failed")
        print("Error: ", e)
        time.sleep(2) """


