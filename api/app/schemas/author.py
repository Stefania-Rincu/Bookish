from pydantic import BaseModel, ConfigDict

class AuthorCreate(BaseModel):
    author_name: str

class AuthorOut(BaseModel):
    id: int
    author_name: str
    model_config = ConfigDict(from_attributes=True)
