from fastapi import APIRouter
from model.book import Book
import fake.book as service

router = APIRouter(prefix = "/book")

@router.get("/")
def get_all() -> list[Book]:
    return service.get_all()

@router.get("/{name}")
def get_one(name) -> Book:
    return service.get_one(name)

# all the remaining endpoints do nothing yet:
@router.post("/")
def create(book: Book) -> Book:
    return service.create(book)

@router.patch("/")
def modify(book: Book) -> Book:
    return service.modify(book)

@router.put("/")
def replace(book: Book) -> Book:
    return service.replace(book)

@router.delete("/{name}")
def delete(name: str):
    return service.delete(name)