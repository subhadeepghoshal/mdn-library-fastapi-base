
import os
os.environ["CRYPTID_UNIT_TEST"] = "true"

import pytest
from model.book import Book
from service import book as code
from error import Missing, Duplicate

@pytest.fixture
def sample() -> Book:
    return Book(title="The Third Chimpanzee",
                summary="The Evolution and Future of the Human Anima",
                author="Jared Diamond")


@pytest.fixture
def fakes() -> list[Book]:
    return code.get_all()


def test_create(sample):
    resp = code.create(sample)
    assert resp == sample


def test_create_duplicate(fakes):
    with pytest.raises(Duplicate) as exc:
        _ = code.create(fakes[0])


def test_get_one(fakes):
    resp = code.get_one(fakes[0].title)
    assert resp == fakes[0]


def test_get_one_missing():
    with pytest.raises(Missing):
        resp = code.get_one("Gilgamesh")


def test_modify(sample):
    sample.summary = "A beautiful book"
    assert code.modify(sample.title, sample) == sample


def test_modify_missing(sample):
    with pytest.raises(Missing) as exc:
        resp = code.modify("Mein Kamf", sample)


def test_delete(sample):
    resp = code.delete(sample.title)
    with pytest.raises(Missing):
        code.get_one(sample.title)

def test_delete_missing():
    with pytest.raises(Missing):
        _ = code.delete("Mein Kamf")
