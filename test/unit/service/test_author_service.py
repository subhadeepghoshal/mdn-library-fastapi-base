import os
os.environ["CRYPTID_UNIT_TEST"] = "true"

import pytest
from model.author import Author
from service import author as code
from error import Missing, Duplicate

@pytest.fixture
def sample() -> Author:
    return Author(name="Jaccob Bronowsky",
                  year_of_birth="1908",
                  year_of_death="1974")

@pytest.fixture
def fakes() -> list[Author]:
    return code.get_all()

@pytest.mark.asyncio(scope="session")
async def test_create(sample):
    resp = await code.create(sample)
    assert resp == sample


@pytest.mark.asyncio(scope="session")
async def test_create_duplicate(fakes):
    with pytest.raises(Duplicate) as exc:
        _ = await code.create(fakes[0])


def test_get_one(fakes):
    resp = code.get_one(fakes[0].name)
    assert resp == fakes[0]


def test_get_one_missing():
    with pytest.raises(Missing):
        resp = code.get_one("Hawking")


def test_modify(sample):
    sample.year_of_birth = "1900"
    assert code.modify(sample.name, sample) == sample


def test_modify_missing(sample):
    with pytest.raises(Missing) as exc:
        resp = code.modify("Mein Kamf", sample)


def test_delete(sample):
    resp = code.delete(sample.name)
    with pytest.raises(Missing):
        code.get_one(sample.name)

def test_delete_missing():
    with pytest.raises(Missing):
        _ = code.delete("Mein Kamf")
