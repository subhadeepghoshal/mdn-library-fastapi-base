from model.book import Book
import fake.book as data


def get_all() -> list[Book]:
    return data.get_all()


def get_one(title: str) -> Book | None:
    return data.get_one(title)


def create(book: Book) -> Book:
    return data.create(book)


def replace(id, book: Book) -> Book:
    return data.replace(id, book)


def modify(id, book: Book) -> Book:
    return data.modify(id, book)


def delete(id, book: Book) -> bool:
    return data.delete(id)