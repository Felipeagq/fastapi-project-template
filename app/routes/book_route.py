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
