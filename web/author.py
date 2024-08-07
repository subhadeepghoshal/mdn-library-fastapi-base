import os
from pathlib import Path

from fastapi import APIRouter, HTTPException

from model.author import Author,AuthorCollection

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import author as service
else:
    from service import author as service

from error import Missing, Duplicate

router = APIRouter(prefix="/author")


@router.get("/")
async def get_all() -> list[Author]:
    authors = await service.get_all()
    return authors

@router.get("/{name}")
async def get_one(name) -> Author:
    try:
        return await service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


# all the remaining endpoints do nothing yet:
@router.post("/", status_code=201)
async def create(author: Author) -> Author:
    try:
        return await service.create(author)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/{name}")
async def modify(name: str, author: Author) -> Author:
    try:
        return await service.modify(name, author)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}")
async def delete(name: str):
    try:
        return await service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)