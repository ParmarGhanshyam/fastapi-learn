from pydantic import BaseModel
from typing import List


class UserData(BaseModel):
    name: str
    email: str
    password: str


class BlogBase(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


# Using Response Model
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[BlogBase] = []

    class Config():
        orm_mode = True


class Datablog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config():
        orm_mode = True
