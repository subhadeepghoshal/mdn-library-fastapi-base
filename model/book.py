from pydantic import BaseModel

class Book(BaseModel):
    title:str
    summary:str
    author:str