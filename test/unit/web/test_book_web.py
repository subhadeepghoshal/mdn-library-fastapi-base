from fastapi import HTTPException
import pytest
import os
os.environ["CRYPTID_UNIT_TEST"] = "true"
from model.book import Book
from web import book
from error import Missing, Duplicate


@pytest.fixture
def sample() -> Book:
    return Book(title="The Third Chimpanzee",
                summary="The Evolution and Future of the Human Anima",
                author="Jared Diamond")

@pytest.fixture
def fakes() -> list[Book]:
    return book.get_all()


def assert_duplicate(exc):
    assert exc.value.status_code == 404
    assert "Duplicate" in exc.value.msg


def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "Missing" in exc.value.msg


def test_create(sample):
    assert book.create(sample) == sample


def test_create_duplicate(fakes):
    with pytest.raises(HTTPException) as exc:
        book.create(fakes[0])
        assert_duplicate(exc)


def test_get_one(fakes):
    assert book.get_one(fakes[0].title) == fakes[0]


def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        book.get_one("Gilgamesh")
        assert_missing(exc)


def test_modify(fakes, sample):
    assert book.modify(fakes[0].title, sample) == sample


def test_modify_missing(sample):
    with pytest.raises(HTTPException) as exc:
        book.modify("Gilgamesh", sample)
        assert_missing(exc)


def test_delete(fakes):
    assert book.delete(fakes[0].title) is True


def test_delete_missing(sample):
    with pytest.raises(HTTPException) as exc:
        book.delete("Gilgamesh")
        assert_missing(exc)
