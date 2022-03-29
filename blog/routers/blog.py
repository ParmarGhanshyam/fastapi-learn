from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from blog.models import Blog
from sqlalchemy.orm import Session
from blog.schemas import Datablog
from blog.dependency import get_db
from blog.routers.authentication import *
from blog.routers.token import *
from blog.oauth2 import get_current_url
from blog.schemas import UserData
from blog.models import User

router = APIRouter(
    prefix="/blog",
    tags=['blog']
)


@router.get('/', response_model=List[Datablog])
def all(db: Session = Depends(get_db), get_current_user : UserData = Depends(get_current_url)):
    blogs = db.query(Blog).all()
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Datablog, db: Session = Depends(get_db), get_current_user : User = Depends(get_current_url)):
    new_blog = Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/{id}', status_code=200, response_model=Datablog)
def show(id, response: Response, db: Session = Depends(get_db),get_current_user : UserData = Depends(get_current_url)):
    blogs = db.query(Blog).filter(Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return blogs


@router.delete('/{id}')
def destroy(id, db: Session = Depends(get_db),get_current_user : UserData = Depends(get_current_url)):
    blogs = db.query(Blog).filter(Blog.id == id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" blog with this id {id}  not exist")
    blogs.delete(synchronize_session=False)
    db.commit()
    return "Deleted"


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: Datablog, db: Session = Depends(get_db),get_current_user : UserData = Depends(get_current_url)):
    # blogs = db.query(Blog).filter(Blog.id == id).update({'title' : 'Ghanshyam data'})
    blogs = db.query(Blog).filter(Blog.id == id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    blogs.update(request.dict())
    db.commit()
    return 'Updated'
