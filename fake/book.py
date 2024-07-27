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


def check_duplicate(name: str):
    if find(name):
        raise Duplicate(msg=f"Duplicate book {name}")


def get_all() -> list[Book]:
    """Return all books"""
    return _books


def get_one(name: str) -> Book:
    """Return one book"""
    for _book in _books:
        if _book.name == name:
            return _book
    raise Missing(msg=f"Book {name} not found")


def create(book: Book) -> Book:
    """Add a book"""
    check_duplicate(book.name)
    _books.append(book)
    return book


def modify(name, book: Book) -> Book:
    """modify a book"""
    check_missing(name)
    for _book in _books:
        if _book.name == name:
            _books.remove(_book)
            _books.append(book)
            return book


def delete(name: str):
    """Delete a book"""
    check_missing(name)
    for _book in _books:
        if _book.name == name:
            _books.remove(_book)
            return True
