import os
from model.author import Author

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import author as data
else:
    from data import author as data

def get_all() -> list[Author]:
    return data.get_all()


def get_one(name: str) -> Author | None:
    return data.get_one(name)


def create(author: Author) -> Author:
    return data.create(author)


def modify(name, author: Author) -> Author:
    return data.modify(name, author)


def delete(name) -> bool:
    return data.delete(name)
