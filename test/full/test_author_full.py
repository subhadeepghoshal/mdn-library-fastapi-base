import pytest
from httpx import AsyncClient
from model.author import Author
from main import app

client = AsyncClient(app=app, base_url="http://127.0.0.1:9000/")

@pytest.fixture(scope="session")
def sample() -> Author:
    return Author(name="Jaccob Bronowsky",
                  year_of_birth="1908",
                  year_of_death="1974")

@pytest.mark.asyncio(scope="session")
async def test_create(sample):
    async with AsyncClient(app=app, base_url="http://127.0.0.1:9000/") as ac:
        resp = await ac.post("/author/",json=sample.model_dump())
    assert resp.status_code == 201

@pytest.mark.asyncio(scope="session")
async def test_create_duplicate(sample):
    resp = await client.post("/author/", json=sample.model_dump())
    assert resp.status_code == 409

@pytest.mark.asyncio(scope="session")
async def test_get_one(sample):
    resp = await client.get(f"/author/{sample.name}")
    resp_json = resp.json()
    resp_json.pop("_id")
    input = sample.model_dump()
    input.pop("id")
    assert resp_json == input
@pytest.mark.asyncio(scope="session")
async def test_get_one_missing():
    resp = await client.get("/author/bobcat")
    assert resp.status_code == 404

@pytest.mark.asyncio(scope="session")
async def test_modify(sample):
    resp = await client.patch(f"/author/{sample.name}", json=sample.model_dump())
    resp_json = resp.json()
    resp_json.pop("_id")
    input = sample.model_dump()
    input.pop("id")
    assert resp_json == input

@pytest.mark.asyncio(scope="session")
async def test_modify_missing(sample):
    resp = await client.patch("/author/alismunro", json=sample.model_dump())
    assert resp.status_code == 404

@pytest.mark.asyncio(scope="session")
async def test_delete(sample):
    resp = await client.delete(f"/author/{sample.name}")
    assert resp.status_code == 200
    assert resp.json() is True

@pytest.mark.asyncio(scope="session")
async def test_delete_missing(sample):
    resp = await client.delete(f"/author/{sample.name}")
    assert resp.status_code == 404
