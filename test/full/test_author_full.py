import pytest
from fastapi.testclient import TestClient
from model.author import Author
from main import app

client = TestClient(app)


@pytest.fixture(scope="session")
def sample() -> Author:
    return Author(name="Jaccob Bronowsky",
                  year_of_birth="1908",
                  year_of_death="1974")


def test_create(sample):
    resp = client.post("/author", json=sample.model_dump())
    assert resp.status_code == 201


def test_create_duplicate(sample):
    resp = client.post("/author", json=sample.model_dump())
    assert resp.status_code == 409


def test_get_one(sample):
    resp = client.get(f"/author/{sample.name}")
    assert resp.json() == sample.model_dump()


def test_get_one_missing():
    resp = client.get("/author/bobcat")
    assert resp.status_code == 404


def test_modify(sample):
    resp = client.patch(f"/author/{sample.name}", json=sample.model_dump())
    assert resp.json() == sample.model_dump()


def test_modify_missing(sample):
    resp = client.patch("/author/alismunro", json=sample.model_dump())
    assert resp.status_code == 404


def test_delete(sample):
    resp = client.delete(f"/author/{sample.name}")
    assert resp.status_code == 200
    assert resp.json() is True


def test_delete_missing(sample):
    resp = client.delete(f"/author/{sample.name}")
    assert resp.status_code == 404
