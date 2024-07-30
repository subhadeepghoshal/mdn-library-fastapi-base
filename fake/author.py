from model.author import Author
from error import Missing, Duplicate

# fake data, until we use a real database and SQL
_authors = [
    Author(name="Chris McManus",
           year_of_birth="1950",
           year_of_death=""),
    Author(name="Mahmood Mamdani",
           year_of_birth="1946",
           year_of_death=""),
]


def find(name: str) -> Author | None:
    for c in _authors:
        if c.name == name:
            return c
    return None


def check_missing(name: str):
    if not find(name):
        raise Missing(msg=f"Missing author {name}")


def check_duplicate(name: str):
    if find(name):
        raise Duplicate(msg=f"Duplicate author {name}")


def get_all() -> list[Author]:
    """Return all authors"""
    return _authors


def get_one(name: str) -> Author:
    """Return one author"""
    for _author in _authors:
        if _author.name == name:
            return _author
    raise Missing(msg=f"Author {name} not found")


def create(author: Author) -> Author:
    """Add a author"""
    check_duplicate(author.name)
    _authors.append(author)
    return author


def modify(name, author: Author) -> Author:
    """modify a author"""
    check_missing(name)
    for _author in _authors:
        if _author.name == name:
            _authors.remove(_author)
            _authors.append(author)
            return author


def delete(name: str):
    """Delete a author"""
    check_missing(name)
    for _author in _authors:
        if _author.name == name:
            _authors.remove(_author)
            return True
