import pytest

from error import Missing
from model.book import Book
from service import book as code

sample = Book(title="Right Hand Left Hand",
              summary="The Origins of Asymmetry in Brains, Bodies, Atoms and Culture",
              author="Chris McManus")


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exists():
    resp = code.get_one("Right Hand Left Hand")
    assert resp == sample


def test_get_missing():
    with pytest.raises(Missing):
        resp = code.get_one("Gilgamesh")
