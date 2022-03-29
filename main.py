from fastapi import FastAPI, Depends, status, Response, HTTPException
# from blog.database import engine
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
# from blog.database import Base
# from .database import Sessionlocal, engine, Base
from sqlalchemy import create_engine
from blog.database import Sessionlocal,engine,Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from blog.schemas import ShowUser, UserData, Datablog
from blog.models import User, Blog
from blog.dependency import get_db

app = FastAPI()
Base.metadata.create_all(engine)


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: Datablog, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=Datablog)
def show(id, response: Response, db: Session = Depends(get_db)):
    blogs = db.query(Blog).filter(Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return blogs


@app.delete('/blog/{id}')
def destroy(id, db: Session = Depends(get_db)):
    blogs = db.query(Blog).filter(Blog.id == id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" blog with this id {id}  not exist")
    blogs.delete(synchronize_session=False)
    db.commit()
    return "Deleted"


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: Datablog, db: Session = Depends(get_db)):
    # blogs = db.query(Blog).filter(Blog.id == id).update({'title' : 'Ghanshyam data'})
    blogs = db.query(Blog).filter(Blog.id == id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    blogs.update(request.dict())
    db.commit()
    return 'Updated'


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post('/user_create', status_code=status.HTTP_201_CREATED, response_model=ShowUser, tags=['user'])
def user_create(request: UserData, db: Session = Depends(get_db)):
    hassing_password = pwd_context.hash(request.password)
    user_create = User(name=request.name, email=request.email, password=hassing_password)
    db.add(user_create)
    db.commit()
    db.refresh(user_create)
    return user_create


@app.get('/user_create/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser, tags=['user'])
def get_user(id, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.id == id).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
        # return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user id is {id} not exist")
    return user_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000, log_level="debug")
