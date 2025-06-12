from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
    
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default to true

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

my_posts = [{"title": "Title of post1", "content": "Content of post1", "id":1},
            {"title": "Favourite foods", "content": "i liek pizza", "id":2}]

@app.get("/")
def root():
    return {"message": "welkem to my api"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts  ORDER BY id ASC""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"post": new_post}

@app.get("/posts/{id}")
def get_post(id: int):  # response:Response
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"post": post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET (title, content, published) = (%s, %s, %s) WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"data" : post}
