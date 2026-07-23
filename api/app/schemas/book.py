from datetime import date
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
    authors: list[str]
    model_config = ConfigDict(from_attributes=True)

class CheckedOutBook(BookOut):
    due_return: date

class PagedBooks(BaseModel):
    items: list[BookOut]
    total: int
    page: int
    page_size: int
