from datetime import date
from pydantic import BaseModel, ConfigDict

class UserBookCreate(BaseModel):
    id_user: int
    id_book: int
    due_return: date

class UserBookOut(BaseModel):
    id: int
    id_user: int
    id_book: int
    due_return: date
    model_config = ConfigDict(from_attributes=True)
