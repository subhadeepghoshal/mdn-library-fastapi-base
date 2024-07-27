import os
import pytest
from model.book import Book
from error import Missing, Duplicate

# set this before data imports below for data.init
os.environ["LIBRARY_SQLITE_DB"] = ":memory:"
from data import book


@pytest.fixture
def sample() -> Book:
    return Book(title="The Third Chimpanzee",
                summary="The Evolution and Future of the Human Anima",
                author="Jared Diamond")


def test_create(sample):
    resp = book.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = book.create(sample)


def test_get_one(sample):
    resp = book.get_one(sample.title)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = book.get_one("boxturtle")


def test_modify(sample):
    sample.summary = "How Our Animal Heritage Affects the Way We Live"
    resp = book.modify(sample.title, sample)
    assert resp == sample


def test_modify_missing():
    thing: Book = Book(title="One, Two, Three to Infinity",
                       summary="One, Two, Three to Infinity",
                       author="George Gamow")
    with pytest.raises(Missing):
        _ = book.modify(thing.title, thing)


def test_delete(sample):
    resp = book.delete(sample.title)
    assert resp is True


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = book.delete(sample.title)
