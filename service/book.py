import os
from model.book import Book,UpdateBook, LanguageEnum

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import book as data
else:
    from data import book as data


async def get_all(language:LanguageEnum) -> list[Book]:
    return await data.get_all(language)

async def get_one(title: str) -> Book | None:
    return await data.get_one(title)


async def create(book: Book) -> Book:
    return await data.create(book)


async def modify(title, book: UpdateBook) -> Book:
    print("200")
    return await data.modify(title, book)


async def delete(title) -> bool:
    return await data.delete(title)
