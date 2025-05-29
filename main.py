from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default to true
    rating: Optional[int] = None  # None isnt an int so use optional

my_posts = [{"title": "Title of post1", "content": "Content of post1", "id":1},
            {"title": "Favourite foods", "content": "i liek pizza", "id":2}]

def find_post(id):
    post_index = {p["id"]: p for p in my_posts}  # dictionary lookup
    return post_index.get(id)

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "welkem to my api"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts} #fastapi changes arrays to json

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post): # schema, validation
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0,100000000000)
    my_posts.append(post_dict)
    return {"post": post_dict}

@app.get("/posts/{id}") # however if we have a /posts/latest or smthing, it will call this function. routing error. order matters here
def get_post(id: int):  # response:Response
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND  # no hardcoding in a number
        # return {"messgae":f"post with id {id} was not found"}
    return {"post": post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    post = my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
