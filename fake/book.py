from model.book import Book
from error import Missing, Duplicate

# fake data, until we use a real database and SQL
_books = [
    Book(title="Right Hand Left Hand",
             summary="The Origins of Asymmetry in Brains, Bodies, Atoms and Culture",
             author="Chris McManus"),
    Book(title="Neither Settler Nor Native",
             summary="The Making and Unmaking of Permanent Minorities",
             author="Mahmood Mamdani"),
]

def find(title: str) -> Book | None:
    for c in _books:
        if c.title == title:
            return c
    return None

def check_missing(tile: str):
    if not find(tile):
        raise Missing(msg=f"Missing book {tile}")


def get_all() -> list[Book]:
    """Return all books"""
    return _books


def get_one(tile: str) -> Book | None:
    """Return one book"""
    for _book in _books:
        if _book.tile == tile:
            return _book
    return None


# The following are nonfunctional for now,
# so they just act like they work, without modifying
# the actual fake _books list:
def create(book: Book) -> Book:
    """Add a book"""
    return book


def modify(book: Book) -> Book:
    """Partially modify a book"""
    return book


def replace(book: Book) -> Book:
    """Completely replace a book"""
    return book


def delete(tile: str):
    """Delete a book; return None if it existed"""
    return None