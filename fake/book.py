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


def check_missing(title: str):
    if not find(title):
        raise Missing(msg=f"Missing book {title}")


def check_duplicate(title: str):
    if find(title):
        raise Duplicate(msg=f"Duplicate book {title}")


def get_all() -> list[Book]:
    """Return all books"""
    return _books


def get_one(title: str) -> Book:
    """Return one book"""
    for _book in _books:
        if _book.title == title:
            return _book
    raise Missing(msg=f"Book {title} not found")


def create(book: Book) -> Book:
    """Add a book"""
    check_duplicate(book.title)
    _books.append(book)
    return book


def modify(title, book: Book) -> Book:
    """modify a book"""
    check_missing(title)
    for _book in _books:
        if _book.title == title:
            _books.remove(_book)
            _books.append(book)
            return book


def delete(title: str):
    """Delete a book"""
    check_missing(title)
    for _book in _books:
        if _book.title == title:
            _books.remove(_book)
            return True
