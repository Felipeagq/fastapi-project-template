# creamos un mongo_crud
```python 
# ./app/database/mongo/mongo_crud.py
from app.schemas import bookSchemas
from app.database.mongo.mongo_core import mg_database
import uuid
from datetime import datetime


class BookCRUDMongo():

    @staticmethod
    async def read_all():
        _book = []
        collection = mg_database["book"].find()
        async for book in collection:
            _book.append(book)
        return _book
    

    @staticmethod
    async def create(
        book: bookSchemas.BookRequestScheme,
        token_id:str
    ) -> str:
        id = str(uuid.uuid4())
        _book = {
            "_id":id,
            "title": book.title,
            "description": book.description,
            "date": str(datetime.now()),
            "autor": token_id
        }
        await mg_database["book"].insert_one(_book)
        return _book


    @staticmethod
    async def delete(
        id:str
    ) -> str:
        _book = await mg_database["book"].delete_one({"_id":id})
        return _book
    

    @staticmethod
    async def update(
        id:str,
        book: bookSchemas.BookRequestScheme,
        token_id:str
    ) -> str:
        _book = await mg_database["book"].find_one({"_id":id})
        _book["title"] = book.title
        _book["description"] = book.description
        _book["autor"] = token_id
        _book["date"] = str(datetime.now())
        await mg_database["book"].update_one({"_id":id},{"$set":_book})
        return _book

```

# creamos schemas de books
```python
# ./app/schemas/bookSchemas.py
from pydantic import BaseModel
from typing import  TypeVar, Optional
T = TypeVar("T")

class BlogRequestScheme(BaseModel):
    title: str
    body: str


class BookRequestScheme(BaseModel):
    title: str
    description: str


class GeneralResponse(BaseModel):
    msg:str
    status:str
    data: Optional[T] = None
```


# creamos el router de book
```python
# ./app/routes/book_route.py
from fastapi import APIRouter, Depends, status, HTTPException

from app.database.mongo.mongo_crud import BookCRUDMongo
from app.schemas import bookSchemas

from app.settings.security import *


router = APIRouter(tags=["Book Managament"])

@router.get("/")
async def get_books():
    _bookList = await BookCRUDMongo.read_all()
    return {
        "status": status.HTTP_202_ACCEPTED,
        "msg":"ok",
        "data": _bookList
    }

@router.post("/")
async def create_book(
    book: bookSchemas.BookRequestScheme,
    token = Depends(get_current_user)
):
    _book = await BookCRUDMongo.create(
        book=book,
        token_id=token.id
    )
    return {
        "status": status.HTTP_202_ACCEPTED,
        "msg":"ok",
        "data": _book
    }

```