from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# ---------------------
# Item Model
# ---------------------
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)  # e.g. tmdb-123 or gb-abc
    name = Column(String, index=True)
    type = Column(String)  # "movie" or "book"
    description = Column(String, nullable=True)
    poster_url = Column(String, nullable=True)

    users = relationship("UserItem", back_populates="item")


# ---------------------
# User Model
# ---------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    items = relationship("UserItem", back_populates="user")


# ---------------------
# UserItem Model
# ---------------------
class UserItem(Base):
    __tablename__ = "user_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    status = Column(String, default="plan")  # plan / reading / watched
    rating = Column(Integer, nullable=True)
    review = Column(String, nullable=True)

    user = relationship("User", back_populates="items")
    item = relationship("Item", back_populates="users")
