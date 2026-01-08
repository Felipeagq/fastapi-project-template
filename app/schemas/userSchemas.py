from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str