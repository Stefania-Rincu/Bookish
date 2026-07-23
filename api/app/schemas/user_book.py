from datetime import date
from pydantic import BaseModel, ConfigDict

class UserBookCreate(BaseModel):
    id_user: int
    id_book: int
    due_return: date
    returned_date: date | None = None

class UserBookOut(BaseModel):
    id: int
    id_user: int
    id_book: int
    due_return: date
    returned_date: date | None = None
    model_config = ConfigDict(from_attributes=True)

class Borrower(BaseModel):
    name: str
    due_return: date
