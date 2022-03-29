from fastapi import APIRouter, Depends, HTTPException,status
from blog.schemas import *
from sqlalchemy.orm import Session
from blog.dependency import get_db
from blog.models import User
from blog.hashing import Hash
from datetime import datetime, timedelta
from blog.routers.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/login",
    tags=['login']
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
@router.post('/')
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session  = Depends(get_db)):
    print(request.username)
    print(request.password)
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Invalid credentials")

    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
