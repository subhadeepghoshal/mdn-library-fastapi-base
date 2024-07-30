import os
from pathlib import Path

from fastapi import APIRouter, HTTPException

from model.author import Author

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import author as service
else:
    from service import author as service

from error import Missing, Duplicate

router = APIRouter(prefix="/author")


@router.get("/")
def get_all() -> list[Author]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Author:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


# all the remaining endpoints do nothing yet:
@router.post("/", status_code=201)
def create(author: Author) -> Author:
    try:
        return service.create(author)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/{name}")
def modify(name: str, author: Author) -> Author:
    try:
        return service.modify(name, author)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}")
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)