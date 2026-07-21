from pydantic import BaseModel, ConfigDict

class BookCreate(BaseModel):
    title: str
    isbn: str
    num_copies: int
    authors: list[str]

class BookOut(BaseModel):
    id: int
    title: str
    isbn: str
    num_copies: int
    model_config = ConfigDict(from_attributes=True)
