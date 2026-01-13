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
        book = {
            "_id":id,
            "title": book.title,
            "description": book.description,
            "date": str(datetime.now()),
            "autor": token_id
        }
        await mg_database["book"].insert_one(book)
        return book


    @staticmethod
    async def delete(
        id:str
    ) -> str:
        book = await mg_database["book"].delete_one({"_id":id})
        return book
    

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