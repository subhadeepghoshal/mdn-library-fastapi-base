import os
import pytest
from model.author import Author
from fastapi import HTTPException, status

from error import Missing, Duplicate

sample_id: str = ""

# set this before data imports below for data.init
os.environ["LIBRARY_SQLITE_DB"] = ":memory:"
from data import author


@pytest.fixture
def sample() -> Author:
    return Author(name="Jaccob Bronowsky",
                  year_of_birth="1908",
                  year_of_death="1974")


@pytest.mark.asyncio(scope="session")
async def test_create(sample):
    global sample_id
    input_author = sample.model_dump()
    input_author.pop("id")
    resp = await author.create(sample)
    sample_id = resp.pop("_id")
    assert resp == input_author


@pytest.mark.asyncio(scope="session")
async def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        await author.create(sample)


#
#
@pytest.mark.asyncio(scope="session")
async def test_get_one(sample):
    input_author = sample.model_dump()
    input_author.pop("id")
    resp = await author.get_one(sample.name)
    resp.pop("_id")
    assert resp == input_author


@pytest.mark.asyncio(scope="session")
async def test_get_one_missing():
    with pytest.raises(Missing):
        await author.get_one("boxturtle")


@pytest.mark.asyncio(scope="session")
async def test_modify(sample):
    sample.year_of_birth = "1907"
    resp = await author.modify(sample.name, sample)
    input_author = sample.model_dump()
    input_author.pop("id")
    resp.pop("_id")
    assert resp == input_author


@pytest.mark.asyncio(scope="session")
async def test_modify_missing():
     thing: Author = Author(name="George Gamow",
                            year_of_birth="1904",
                            year_of_death="1968")
     with pytest.raises(Missing):
         await author.modify(thing.name, thing)
#
#
@pytest.mark.asyncio(scope="session")
async def test_delete(sample):
    resp = await author.delete(sample.name)
    assert resp is True


@pytest.mark.asyncio(scope="session")
async def test_delete_missing(sample):
    with pytest.raises(Missing):
        await author.delete(sample.name)
