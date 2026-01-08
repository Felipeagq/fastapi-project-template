from pydantic import BaseModel
from typing import  TypeVar, Optional

class BlogRequestScheme(BaseModel):
    title: str
    body: str


class BookRequestScheme(BaseModel):
    title: str
    description: str
