import os
from pathlib import Path

from fastapi import APIRouter, HTTPException

from model.book import Book, UpdateBook

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import book as service
else:
    from service import book as service

from error import Missing, Duplicate

router = APIRouter(prefix="/book")


@router.get("/")
async def get_all() -> list[Book]:
    books = await service.get_all()
    return books

@router.get("/{title}")
async def get_one(title) -> Book:
    try:
        return await service.get_one(title)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


# all the remaining endpoints do nothing yet:
@router.post("/", status_code=201)
async def create(book: Book) -> Book:
    try:
        return await service.create(book)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/{title}")
async def modify(title: str, book: UpdateBook) -> Book:
    try:
        print("100")
        return await service.modify(title, book)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{title}")
async def delete(title: str):
    try:
        return await service.delete(title)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)