import sqlite3
from .init import curs, IntegrityError
from model.author import Author
from error import Missing, Duplicate

curs.execute("""create table if not exists author(
                name text primary key,
                year_of_birth text,
                year_of_death text)""")


def row_to_model(row: tuple) -> Author:
    name, year_of_birth, year_of_death = row
    return Author(name=name, year_of_birth=year_of_birth, year_of_death=year_of_death)


def model_to_dict(author: Author) -> dict:
    return author.model_dump()


def get_one(name: str) -> Author:
    qry = "select * from author where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Author {name} not found")


def get_all() -> list[Author]:
    qry = "select * from author"
    curs.execute(qry)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(author: Author):
    qry = """insert into author values
          (:name, :year_of_birth, :year_of_death)"""
    params = model_to_dict(author)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"Author {author.name} already exists")
    return get_one(author.name)


def modify(name: str, author: Author) -> Author:
    qry = """update author
             set year_of_birth=:year_of_birth,
                 year_of_death=:year_of_death
             where name=:name_orig"""
    params = model_to_dict(author)
    params["name_orig"] = name
    _ = curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(author.name)
    else:
        raise Missing(msg=f"Author {name} not found")


def delete(name: str):
    qry = "delete from author where name = :name"
    params = {"name": name}
    res = curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Author {name} not found")
    return bool(res)
