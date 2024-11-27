# import sqlite3

from bson import ObjectId
from pymongo import ReturnDocument

from error import Duplicate, Missing
from model.book import Book, UpdateBook
from .init import db

book_collection = db.get_collection("books")


def row_to_model(row: tuple) -> Book:
    title, summary, author = row
    return Book(title=title, summary=summary, author=author)


def model_to_dict(book: Book) -> dict:
    return book.model_dump()


async def get_one(title: str) -> Book:
    if (book := await book_collection.find_one({"title": title})) is not None:
        return book

    raise Missing(msg=f"Book {title} not found")


async def get_all() -> list[Book]:
    books = await book_collection.find().to_list(1000)
    return books


async def create(book: Book) -> Book:
    if await book_collection.find_one({"title": book.title}):
        raise Duplicate(msg=f"Book {book.title} already exists")

    new_book = await book_collection.insert_one(book.model_dump(by_alias=True, exclude=["id"]))
    added_book = await book_collection.find_one({"_id": new_book.inserted_id})
    return added_book


async def modify(title: str, book: UpdateBook) -> Book:
    print(book)
    existing_book = await get_one(title)

    book_updates = {k: v for k, v in book.model_dump(by_alias=True).items() if v is not None}

    if len(book_updates) >= 1:
        update_result = await book_collection.find_one_and_update({"_id": ObjectId(existing_book["_id"])},
            {"$set": book_updates}, return_document=ReturnDocument.AFTER, )

        return update_result


async def delete(title: str):
    delete_result = await book_collection.delete_one({"title": title})
    if delete_result.deleted_count == 1:
        return True

    raise Missing(msg=f"Book '{title}' not found")
