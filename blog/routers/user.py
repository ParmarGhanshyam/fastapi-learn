from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from blog.models import Blog, User
from blog.schemas import UserData, ShowUser
from blog.dependency import get_db
from blog.hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowUser)
def user_create(request: UserData, db: Session = Depends(get_db)):
    user_create = User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(user_create)
    db.commit()
    db.refresh(user_create)
    return user_create


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser)
def get_user(id, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.id == id).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
        # return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user id is {id} not exist")
    return user_data
