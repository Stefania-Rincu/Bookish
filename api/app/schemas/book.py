from datetime import date
from pydantic import BaseModel, ConfigDict

from app.schemas.user_book import Borrower

class BookBase(BaseModel):
    title: str
    isbn: str
    num_copies: int
    authors: list[str]
    
class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CheckedOutBook(BookOut):
    due_return: date

class PagedBooks(BaseModel):
    items: list[BookOut]
    total: int
    page: int
    page_size: int

class BookAvailability(BaseModel):
    id: int
    title: str
    isbn: str
    authors: list[str]
    num_copies: int
    available_copies: int
    borrowers: list[Borrower]
