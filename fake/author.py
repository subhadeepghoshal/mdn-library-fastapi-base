from model.author import Author
from error import Missing, Duplicate

# fake data, until we use a real database and SQL
_authors = [
    Author(_id="100",
           name="Chris McManus",
           year_of_birth="1950",
           year_of_death=""),
    Author(_id=101,
           name="Mahmood Mamdani",
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


async def get_one(name: str) -> dict:
    """Return one author"""
    for _author in _authors:
        if _author.name == name:
            return _author.model_dump()
    raise Missing(msg=f"Author {name} not found")


async def create(author: Author) -> dict:
    """Add a author"""
    check_duplicate(author.name)
    _authors.append(author)
    return author.model_dump()


async def modify(name, author: Author) -> dict:
    """modify a author"""
    check_missing(name)
    for _author in _authors:
        if _author.name == name:
            _authors.remove(_author)
            _authors.append(author)
            return author.model_dump()


async def delete(name: str):
    """Delete a author"""
    check_missing(name)
    for _author in _authors:
        if _author.name == name:
            _authors.remove(_author)
            return True
