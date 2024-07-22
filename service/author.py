from model.author import Author
import fake.author as data


def get_all() -> list[Author]:
    return data.get_all()


def get_one(name: str) -> Author | None:
    return data.get_one(name)


def create(book: Author) -> Author:
    return data.create(book)


def replace(id, book: Author) -> Author:
    return data.replace(id, book)


def modify(id, book: Author) -> Author:
    return data.modify(id, book)


def delete(id, book: Author) -> bool:
    return data.delete(id)