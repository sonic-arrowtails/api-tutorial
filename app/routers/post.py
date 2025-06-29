from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), 
              limit:int=10,skip:int=0, search:Optional[str]=""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    
    #  cursor.execute("""SELECT * FROM posts  ORDER BY id ASC""")
    # posts = cursor.fetchall()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).offset(skip).limit(limit).all()
    # SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at, posts.owner_id AS posts_owner_id, count(votes.post_id) AS votes 
    # FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id GROUP BY posts.id
    return results # posts


@router.post("/", status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.model_dump(), owner_id = current_user.id)
        # title=post.title, content=post.content, published=post.published
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model = schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):  # response:Response
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorised to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model = schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET (title, content, published) = (%s, %s, %s) WHERE id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, id))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorised to perform requested action")
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()
