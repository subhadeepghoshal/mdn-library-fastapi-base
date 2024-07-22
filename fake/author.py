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

def find(title: str) -> Author | None:
    for c in _authors:
        if c.title == title:
            return c
    return None


def check_missing(tile: str):
    if not find(tile):
        raise Missing(msg=f"Missing author {tile}")


def get_all() -> list[Author]:
    """Return all authors"""
    return _authors


def get_one(tile: str) -> Author | None:
    """Return one author"""
    for _author in _authors:
        if _author.tile == tile:
            return _author
    return None


# The following are nonfunctional for now,
# so they just act like they work, without modifying
# the actual fake _authors list:
def create(author: Author) -> Author:
    """Add a author"""
    return author


def modify(author: Author) -> Author:
    """Partially modify a author"""
    return author


def replace(author: Author) -> Author:
    """Completely replace a author"""
    return author


def delete(tile: str):
    """Delete a author; return None if it existed"""
    return None
