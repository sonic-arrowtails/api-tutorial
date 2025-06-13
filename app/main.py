from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

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

my_posts = [{"title": "Title of post1", "content": "Content of post1", "id":1},
            {"title": "Favourite foods", "content": "i liek pizza", "id":2}]

@app.get("/")
def root():
    return {"message": "welkem to my api"}

@app.get("/posts", response_model = List[schemas.Post])
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() 
    # cursor.execute("""SELECT * FROM posts  ORDER BY id ASC""")
    # posts = cursor.fetchall()
    return posts


@app.post("/posts", status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
        # title=post.title, content=post.content, published=post.published
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",response_model = schemas.Post)
def get_post(id: int,db: Session = Depends(get_db)):  # response:Response
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model = schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET (title, content, published) = (%s, %s, %s) WHERE id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, id))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()
