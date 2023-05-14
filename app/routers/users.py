
import email
import  app.models as models, app.schemas as schemas, app.utils as utils, app.oauth2 as oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from app.database import engine,get_db

router = APIRouter(
    prefix= "/users",
    tags= ['Users']
)

@router.post("/",status_code= status.HTTP_201_CREATED,response_model= schemas.UserOut)

def create_user(user :schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password stored in user.password

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user= models.User(**user.dict())
    not_new_user = db.query(models.User).filter(models.User.email == new_user.email).first()
    if not_new_user:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"User with same email: {new_user.email} found")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model= schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} not found")
    return user