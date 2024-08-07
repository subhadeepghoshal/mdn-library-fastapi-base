from fastapi import HTTPException
import pytest
import os
#os.environ["CRYPTID_UNIT_TEST"] = "true"
from model.author import Author
from web import author
from error import Missing, Duplicate


@pytest.fixture
def sample() -> Author:
    return Author(name="Jacob Bronowsky",
                  year_of_birth="1908",
                  year_of_death="1974")


def assert_duplicate(exc):
    assert exc.value.status_code == 404
    assert "Duplicate" in exc.value.msg


def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "Missing" in exc.value.msg


@pytest.mark.asyncio(scope="session")
async def test_create(sample):
    resp = await author.create(sample)
    input_author = sample.model_dump()
    input_author.pop("id")
    resp.pop("_id") if "_id" in resp else resp.pop("id")
    assert resp == input_author


@pytest.mark.asyncio(scope="session")
async def test_create_duplicate(sample):
    with pytest.raises(HTTPException) as exc:
        await author.create(sample)
        assert_duplicate(exc)


@pytest.mark.asyncio(scope="session")
async def test_get_one(sample):
    resp = await author.get_one(sample.name)
    input_author = sample.model_dump()
    input_author.pop("id")
    resp.pop("_id") if "_id" in resp else resp.pop("id")
    assert resp == input_author


@pytest.mark.asyncio(scope="session")
async def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        await author.get_one("weinberg")
        assert_missing(exc)


@pytest.mark.asyncio(scope="session")
async def test_modify(sample):
    sample.year_of_birth = "29/02/2002"
    resp = await author.modify(sample.name, sample)
    input_author = sample.model_dump()
    input_author.pop("id")
    resp.pop("_id") if "_id" in resp else resp.pop("id")
    assert resp == input_author

@pytest.mark.asyncio(scope="session")
async def test_modify_missing(sample):
    with pytest.raises(HTTPException) as exc:
        await author.modify("weinberg", sample)
        assert_missing(exc)

@pytest.mark.asyncio(scope="session")
async def test_delete(sample):
    assert await author.delete(sample.name) is True

@pytest.mark.asyncio(scope="session")
async def test_delete_missing(sample):
    with pytest.raises(HTTPException) as exc:
        await author.delete("weinberg")
        assert_missing(exc)
