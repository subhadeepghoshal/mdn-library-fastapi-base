from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]
from bson import ObjectId


class Book(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    summary: str = Field(...)
    author: str = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "Rise and Fall of 3rd Chimpanzee",
                "summary": "A comprehensive study of human behaviour and its origins. \
                            This book analyses the relationship that human beings have \
                            with their surroundings, along with the cultural aspects involved",
                "author": "Jared Diamond",
            }
        },
    )

class BookCollection(BaseModel):
    authors: List[Book]

class UpdateBook(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    author: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "Rise and Fall of 3rd Chimpanzee",
                "summary": "A comprehensive study of human behaviour and its origins. \
                            This book analyses the relationship that human beings have \
                            with their surroundings, along with the cultural aspects involved",
                "author": "Jared Diamond",
            }
        },
    )