from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:
#     try:  # hardcoding is bad
#         conn = psycopg2.connect(host='localhost', database = 'fastapi', user = 'postgres', password = 'postgres',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Database connection unsuccessful")
#         print("Error:", error)
#         time.sleep(3)
