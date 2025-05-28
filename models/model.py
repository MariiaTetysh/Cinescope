from pydantic import BaseModel


class UserRegistration(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[str]

class UserCreation(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: str
    email: str
    fullName: str
    roles: list[str]
    verified: bool
    createdAt: str
    banned: bool

# class Movie(BaseModel):

