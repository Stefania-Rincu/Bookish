from pydantic import BaseModel, ConfigDict

class AuthorBookCreate(BaseModel):
    id_author: int
    id_book: int

class AuthorBookOut(BaseModel):
    id: int
    id_author: int
    id_book: int
    model_config = ConfigDict(from_attributes=True)
