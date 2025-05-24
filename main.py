from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default to true
    rating: Optional[int] = None  # None isnt an int so use optional

# global variable to store posts
my_posts = [{"title": "Title of post1", "content": "Content of post1", "id":1},
            {"title": "Favourite foods", "content": "i liek pizza", "id":2}]

@app.get("/")
def root():
    return {"message": "welkem to my api"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts} #fastapi changes arrays to json

@app.post("/posts") # naming convention
def create_posts(post: Post): # schema, validation
    print(post)  # title='top beches in florida' content='yo chek this out'
    print(post.title)
    print(post.content)
    print(post.published)
    print(post.model_dump())  #used to be dict()
    return {"post": post}

