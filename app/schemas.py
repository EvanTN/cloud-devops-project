# app/schemas.py
from pydantic import BaseModel
from typing import Optional

# ------------------------
# Item Schemas
# ------------------------
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: Optional[str] = None       # 'book' or 'movie'
    externalId: Optional[str] = None
    posterUrl: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True  # <-- fixed, must be orm_mode for SQLAlchemy


# ------------------------
# User Schemas
# ------------------------
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str


# ------------------------
# User Item Schema (for /user/items)
# ------------------------
class UserItemOut(Item):
    id: int
    name: str
    description: Optional[str] = None
    type: str
    externalId: Optional[str] = None
    posterUrl: Optional[str] = None

    class Config:
        orm_mode = True
