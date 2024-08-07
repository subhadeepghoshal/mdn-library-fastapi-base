import os

os.environ["CRYPTID_UNIT_TEST"] = "True"

import pytest
from model.author import Author,AuthorCollection
from service import author as code
from error import Missing, Duplicate


@pytest.fixture
def sample() -> Author:
    return Author(name="Jaccob Bronowsky",
                  year_of_birth="1908",
                  year_of_death="1974")


@pytest.fixture
async def fakes() -> list[Author]:
    return await code.get_all()


@pytest.mark.asyncio(scope="session")
async def test_create(sample):
    resp = await code.create(sample)
    input_author = sample.model_dump()
    input_author.pop("id")
    resp.pop("_id") if "_id" in resp else resp.pop("id")
    assert resp == input_author


@pytest.mark.asyncio(scope="session")
async def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        await code.create(sample)


@pytest.mark.asyncio(scope="session")
async def test_get_one(sample):
    resp = await code.get_one(sample.name)
    input_author = sample.model_dump()
    input_author.pop("id")
    resp.pop("_id") if "_id" in resp else resp.pop("id")
    assert resp == input_author


@pytest.mark.asyncio(scope="session")
async def test_get_one_missing():
    with pytest.raises(Missing):
        await code.get_one("Hawking")


@pytest.mark.asyncio(scope="session")
async def test_modify(sample):
    sample.year_of_birth = "1900"
    resp = await code.modify(sample.name, sample)
    input_author = sample.model_dump()
    input_author.pop("id")
    resp.pop("_id") if "_id" in resp else resp.pop("id")
    assert resp == input_author


@pytest.mark.asyncio(scope="session")
async def test_modify_missing(sample):
    with pytest.raises(Missing) as exc:
        await code.modify("Mein Kamf", sample)


@pytest.mark.asyncio(scope="session")
async def test_delete(sample):
    await code.delete(sample.name)
    with pytest.raises(Missing):
        await code.get_one(sample.name)

@pytest.mark.asyncio(scope="session")
async def test_delete_missing():
    with pytest.raises(Missing):
        await code.delete("Mein Kamf")
