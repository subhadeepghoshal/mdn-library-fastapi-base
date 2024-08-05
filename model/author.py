from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]
from bson import ObjectId

class Author(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    year_of_birth: str = Field(...)
    year_of_death: str = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "year_of_birth": "12/01/1905",
                "year_of_death": "11/09/1995",
            }
        },
    )


class AuthorCollection(BaseModel):
    authors: List[Author]


class UpdateAuthor(BaseModel):
    name: Optional[str] = None
    year_of_birth: Optional[str] = None
    year_of_death: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "year_of_birth": "12/01/1905",
                "year_of_death": "11/09/1995",
            }
        },
    )