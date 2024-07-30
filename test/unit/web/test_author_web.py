from fastapi import HTTPException
import pytest
import os
os.environ["CRYPTID_UNIT_TEST"] = "true"
from model.author import Author
from web import author
from error import Missing, Duplicate


@pytest.fixture
def sample() -> Author:
    return Author(name="Jaccob Bronowsky",
                  year_of_birth="1908",
                  year_of_death="1974")


@pytest.fixture
def fakes() -> list[Author]:
    return author.get_all()


def assert_duplicate(exc):
    assert exc.value.status_code == 404
    assert "Duplicate" in exc.value.msg


def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "Missing" in exc.value.msg


def test_create(sample):
    assert author.create(sample) == sample


def test_create_duplicate(fakes):
    with pytest.raises(HTTPException) as exc:
        author.create(fakes[0])
        assert_duplicate(exc)


def test_get_one(fakes):
    assert author.get_one(fakes[0].name) == fakes[0]


def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        author.get_one("weinberg")
        assert_missing(exc)


def test_modify(fakes, sample):
    assert author.modify(fakes[0].name, sample) == sample


def test_modify_missing(sample):
    with pytest.raises(HTTPException) as exc:
        author.modify("weinberg", sample)
        assert_missing(exc)


def test_delete(fakes):
    assert author.delete(fakes[0].name) is True


def test_delete_missing(sample):
    with pytest.raises(HTTPException) as exc:
        author.delete("weinberg")
        assert_missing(exc)
