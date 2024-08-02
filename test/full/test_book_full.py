import pytest
from fastapi.testclient import TestClient
from model.book import Book
from main import app

client = TestClient(app)

@pytest.fixture(scope="session")
def sample() -> Book:
    return Book(title="The Third Chimpanzee",
                summary="The Evolution and Future of the Human Anima",
                author="Jared Diamond")

def test_create(sample):
    resp = client.post("/book", json=sample.model_dump())
    assert resp.status_code == 201

def test_create_duplicate(sample):
    resp = client.post("/book", json=sample.model_dump())
    assert resp.status_code == 409

def test_get_one(sample):
    resp = client.get(f"/book/{sample.title}")
    assert resp.json() == sample.model_dump()

def test_get_one_missing():
    resp = client.get("/book/bobcat")
    assert resp.status_code == 404

def test_modify(sample):
    resp = client.patch(f"/book/{sample.title}", json=sample.model_dump())
    assert resp.json() == sample.model_dump()

def test_modify_missing(sample):
    resp = client.patch("/book/rougarou", json=sample.model_dump())
    assert resp.status_code == 404

def test_delete(sample):
    resp = client.delete(f"/book/{sample.title}")
    assert resp.status_code == 200
    assert resp.json() is True

def test_delete_missing(sample):
    resp = client.delete(f"/book/{sample.title}")
    assert resp.status_code == 404