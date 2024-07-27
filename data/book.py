import sqlite3
from .init import curs, IntegrityError
from model.book import Book
from error import Missing, Duplicate

curs.execute("""create table if not exists book(
                title text primary key,
                summary text,
                author text)""")


def row_to_model(row: tuple) -> Book:
    title, summary, author = row
    return Book(title=title, summary=summary, author=author)


def model_to_dict(book: Book) -> dict:
    return book.model_dump()


def get_one(title: str) -> Book:
    qry = "select * from book where title=:title"
    params = {"title": title}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Book {title} not found")


def get_all() -> list[Book]:
    qry = "select * from book"
    curs.execute(qry)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(book: Book):
    qry = """insert into book values
          (:title, :summary, :author)"""
    params = model_to_dict(book)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=
                        f"Book {book.title} already exists")
    return get_one(book.title)


def modify(title: str, book: Book) -> Book:
    qry = """update book
             set summary=:summary,
                 author=:author
             where title=:title_orig"""
    params = model_to_dict(book)
    params["title_orig"] = title
    _ = curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(book.title)
    else:
        raise Missing(msg=f"Book {title} not found")


def delete(title: str):
    qry = "delete from book where title = :title"
    params = {"title": title}
    res = curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Book {title} not found")
    return bool(res)
