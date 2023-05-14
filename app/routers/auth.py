
from fastapi import APIRouter,HTTPException , Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine,get_db
import schemas
import models
import utils
import oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login',response_model= schemas.Token)
def login(user_creds : OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail ="Invaild Credentials")
    if not utils.verify(user_creds.password,user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail ="Invaild Credentials")  
    #create token
    #return token
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    return {"access_token": access_token, "token_type": "bearer"}