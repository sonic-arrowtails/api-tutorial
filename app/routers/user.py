from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)): #dosnt validate repeated email
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    try: #temp
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ts email alr exist twin")

@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with id {id} not found")
    return user
