from pydantic import BaseModel

class Author(BaseModel):
    name:str
    year_of_birth:str
    year_of_death:str
