from fastapi import APIRouter
from model.author import Author
import fake.author as service

router = APIRouter(prefix = "/author")

@router.get("/")
def get_all() -> list[Author]:
    return service.get_all()

@router.get("/{title}")
def get_one(title) -> Author:
    return service.get_one(title)

# all the remaining endpoints do nothing yet:
@router.post("/")
def create(author: Author) -> Author:
    return service.create(author)

@router.patch("/")
def modify(author: Author) -> Author:
    return service.modify(author)

@router.put("/")
def replace(author: Author) -> Author:
    return service.replace(author)

@router.delete("/{title}")
def delete(name: str):
    return service.delete(tile)