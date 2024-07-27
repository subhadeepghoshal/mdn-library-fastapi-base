import os
from model.book import Book

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import book as data
else:
    from data import book as data


def get_all() -> list[Book]:
    return data.get_all()


def get_one(title: str) -> Book | None:
    return data.get_one(title)


def create(book: Book) -> Book:
    return data.create(book)


def modify(title, book: Book) -> Book:
    return data.modify(title, book)


def delete(title) -> bool:
    return data.delete(title)
