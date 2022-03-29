from pydantic import BaseModel


class UserData(BaseModel):
    name: str
    email: str
    password: str


# Using Response Model
class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class Datablog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config():
        orm_mode = True
