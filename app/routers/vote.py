from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(prefix="/vote",tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)  #user can like own post atm
def vote (vote: schemas.Vote, db: Session = Depends(get_db), current_user :schemas.UserOut = Depends(oauth2.get_current_user)):
    print(type(current_user))

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user {vote.user_id} has aleady voted on post {vote.post_id}")
        new_vote = models.Vote(user_id=current_user.id,post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user {vote.user_id} has not voted on post {vote.post_id}, vote doesnt exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}
