import sqlite3

from pymongo import ReturnDocument

from .init import db
from model.author import Author, AuthorCollection
from error import Missing, Duplicate
from bson import ObjectId
from fastapi import HTTPException, status

author_collection = db.get_collection("authors")


def row_to_model(row: tuple) -> Author:
    name, year_of_birth, year_of_death = row
    return Author(name=name, year_of_birth=year_of_birth, year_of_death=year_of_death)


def model_to_dict(author: Author) -> dict:
    return author.model_dump()


async def create(author: Author) -> Author:
    if await author_collection.find_one({"name": author.name}):
        raise Duplicate(msg=f"Author {author.name} already exists")

    new_author = await author_collection.insert_one(
        author.model_dump(by_alias=True, exclude=["id"])
    )
    created_author = await author_collection.find_one(
        {"_id": new_author.inserted_id}
    )
    return created_author


async def get_one(name: str) -> Author:
    if (author := await author_collection.find_one({"name": name})) is not None:
        return author

    raise Missing(msg=f"Author {name} not found")


async def get_all() -> list[Author]:
    authors = await author_collection.find().to_list(1000)
    return authors


#
async def modify(name: str, author: Author) -> Author:
    """ Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    existing_author = await get_one(name)

    author_updates = {
        k: v for k, v in author.model_dump(by_alias=True).items() if v is not None
    }

    if len(author_updates) >= 1:
        update_result = await author_collection.find_one_and_update(
            {"_id": ObjectId(existing_author["_id"])},
            {"$set": author_updates},
            return_document=ReturnDocument.AFTER,
        )

        return update_result

    # The update is empty, but we should still return the matching document:
    return existing_author


async def delete(name: str) -> bool:
    delete_result = await author_collection.delete_one({"name": name})
    if delete_result.deleted_count == 1:
        return True

    raise Missing(msg=f"Author {name} not found")
