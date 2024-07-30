import os
import pytest
from model.author import Author
from error import Missing, Duplicate

# set this before data imports below for data.init
os.environ["LIBRARY_SQLITE_DB"] = ":memory:"
from data import author


@pytest.fixture
def sample() -> Author:
    return Author(name="Jaccob Bronowsky",
                  year_of_birth="1908",
                  year_of_death="1974")


def test_create(sample):
    resp = author.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = author.create(sample)


def test_get_one(sample):
    resp = author.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = author.get_one("boxturtle")


def test_modify(sample):
    sample.year_of_birth = "1907"
    resp = author.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing: Author = Author(name="George Gamow",
                           year_of_birth="1904",
                           year_of_death="1968")
    with pytest.raises(Missing):
        _ = author.modify(thing.name, thing)


def test_delete(sample):
    resp = author.delete(sample.name)
    assert resp is True


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = author.delete(sample.name)