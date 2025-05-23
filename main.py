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

@app.get("/")
def root():
    return {"message": "welkem to my api"}

@app.get("/posts")
def get_posts():
    return {"data": "this is your post)"}

@app.post("/createposts")
def create_posts(new_post: Post): # schema, validation
    print(new_post)  # title='top beches in florida' content='yo chek this out'
    print(new_post.title)
    print(new_post.content)
    print(new_post.published)

    print(new_post.model_dump())  #used to be dict()
    return {"new_post": "new post"}

