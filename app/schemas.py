from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

# For registration
class UserCreate(BaseModel):
    username: str
    password: str

# For returning user info (without password)
class UserOut(BaseModel):
    username: str