# import sqlite3

from error import Duplicate, Missing
from model.book import Book
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


async def modify(title: str, book: Book) -> Book:
    pass # Tobe implemented

async def delete(title: str):
    pass # Tobe implemented
