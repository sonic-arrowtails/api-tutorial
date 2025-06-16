from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from.routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
    
app = FastAPI()

while True:
    try:  # hardcoding is bad
        conn = psycopg2.connect(host='localhost', database = 'fastapi', user = 'postgres', password = 'postgres',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Database connection unsuccessful")
        print("Error:", error)
        time.sleep(3)

# my_posts = [{"title": "Title of post1", "content": "Content of post1", "id":1},
#             {"title": "Favourite foods", "content": "i liek pizza", "id":2}]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "welkem to my api"}