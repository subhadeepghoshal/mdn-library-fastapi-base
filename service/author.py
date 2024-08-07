import os
from model.author import Author, AuthorCollection

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import author as data
else:
    from data import author as data


async def get_all() -> list[Author]:
    authors = await data.get_all()
    return authors

async def get_one(name: str) -> Author | None:
    return await data.get_one(name)


async def create(author: Author) -> Author:
    return await data.create(author)


async def modify(name, author: Author) -> Author:
    return await data.modify(name, author)


async def delete(name) -> bool:
    return await data.delete(name)
