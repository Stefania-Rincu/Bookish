from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    last_name: str
    first_name: str
    username: str
    password_hash: str

class UserOut(BaseModel):
    id: int
    last_name: str
    first_name: str
    username: str
    model_config = ConfigDict(from_attributes=True)
