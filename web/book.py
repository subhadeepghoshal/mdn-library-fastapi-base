import os
from pathlib import Path

from fastapi import APIRouter, HTTPException

from model.book import Book

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import book as service
else:
    from service import book as service

from error import Missing, Duplicate

router = APIRouter(prefix="/book")


@router.get("/")
def get_all() -> list[Book]:
    return service.get_all()


@router.get("/{title}")
def get_one(title) -> Book:
    try:
        return service.get_one(title)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


# all the remaining endpoints do nothing yet:
@router.post("/", status_code=201)
def create(book: Book) -> Book:
    try:
        return service.create(book)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/{title}")
def modify(title: str, book: Book) -> Book:
    try:
        return service.modify(title, book)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{title}")
def delete(title: str):
    try:
        return service.delete(title)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)