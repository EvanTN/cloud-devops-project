from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import SessionLocal
from app import models, schemas
from sqlalchemy import text

# Auth imports
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import httpx
import os
from fastapi import Query

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React dev
        "https://projectevan.vercel.app",
        "https://cloud-project-front-end.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Auth Configuration
# =========================
SECRET_KEY = "supersecretkey"  # 🔒 move to env var in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# =========================
# Pydantic Schemas
# =========================
class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    username: str



# =========================
# Utility Functions
# =========================


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = (
            db.query(models.User)
            .filter(models.User.username == username)
            .first()
        )

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
# ==============
# Table Check
# ==============

@app.get("/debug/tables")
def debug_tables(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """))

    return [row[0] for row in result]

@app.get("/debug/users")
def debug_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return [
        {
            "id": u.id,
            "username": u.username
        }
        for u in users
    ]


@app.get("/debug/users/raw")
def debug_users_raw(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM users"))
    return [dict(row._mapping) for row in result]

# =========================
# Auth Endpoints
# =========================
@app.post("/auth/register", response_model=Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Return token immediately
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/auth/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .first()
    )

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return {"username": current_user.username}


# =========================
# Health Endpoint
# =========================
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


# =========================
# Protected Item Endpoints
# =========================
# @app.post("/items/", response_model=schemas.Item)
# def create_item(
#     item: schemas.ItemCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user),
# ):
#     db_item = models.Item(
#         name=item.name,
#         description=item.description,
#     )

#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)

#     return db_item


# @app.get("/items/{item_id}", response_model=schemas.Item)
# def read_item(
#     item_id: int,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user),
# ):
#     item = db.query(models.Item).filter(models.Item.id == item_id).first()

#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")

#     return item


# @app.get("/items/", response_model=List[schemas.Item])
# def list_items(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user),
# ):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# @app.delete("/items/{item_id}", status_code=204)
# def delete_item(
#     item_id: int,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user),
# ):
#     item = db.query(models.Item).filter(models.Item.id == item_id).first()

#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")

#     db.delete(item)
#     db.commit()










#=======================================









# =========================
# TMDB API + Functions
# =========================
TMDB_API_KEY = os.getenv("TMDB_API_KEY") 
GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"

@app.get("/search")
def search(query: str = Query(...), type: str = Query("all")):
    results = []

    # Search movies via TMDb
    if type in ["all", "movie"]:
        tmdb_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
        with httpx.Client() as client:
            r = client.get(tmdb_url)
            data = r.json()
            for m in data.get("results", []):
                results.append({
                    "externalId": f"tmdb-{m['id']}",
                    "title": m["title"],
                    "description": m.get("overview"),
                    "posterUrl": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}" if m.get("poster_path") else None,
                    "type": "movie"
                })

    # Search books via Google Books
    if type in ["all", "book"]:
        gb_url = f"{GOOGLE_BOOKS_API}?q={query}"
        with httpx.Client() as client:
            r = client.get(gb_url)
            data = r.json()
            for b in data.get("items", []):
                volume = b.get("volumeInfo", {})
                results.append({
                    "externalId": f"gb-{b['id']}",
                    "title": volume.get("title"),
                    "description": volume.get("description"),
                    "posterUrl": volume.get("imageLinks", {}).get("thumbnail"),
                    "type": "book"
                })

    return results

@app.post("/user/items")
def add_user_item(
    external_id: str,
    title: str,
    type: str,
    poster_url: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Check if the item exists in DB
    item = db.query(models.Item).filter(models.Item.external_id == external_id).first()
    if not item:
        item = models.Item(
            external_id=external_id,
            name=title,
            type=type,
            poster_url=poster_url
        )
        db.add(item)
        db.commit()
        db.refresh(item)

    # Check if user already has this item
    existing_user_item = db.query(models.UserItem).filter(
        models.UserItem.user_id == current_user.id,
        models.UserItem.item_id == item.id
    ).first()

    if existing_user_item:
        return existing_user_item

    # Add to user's list
    user_item = models.UserItem(
        user_id=current_user.id,
        item_id=item.id,
        status="plan"
    )
    db.add(user_item)
    db.commit()
    db.refresh(user_item)

    return user_item

@app.get("/user/items", response_model=List[schemas.UserItemOut])
def list_user_items(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user_items = db.query(models.UserItem).filter(models.UserItem.user_id == current_user.id).all()
    return user_items

@app.put("/user/items/{user_item_id}")
def update_user_item(
    user_item_id: int,
    status: Optional[str] = None,
    rating: Optional[int] = None,
    review: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user_item = db.query(models.UserItem).filter(
        models.UserItem.id == user_item_id,
        models.UserItem.user_id == current_user.id
    ).first()

    if not user_item:
        raise HTTPException(status_code=404, detail="User item not found")

    if status:
        user_item.status = status
    if rating:
        user_item.rating = rating
    if review:
        user_item.review = review

    db.commit()
    db.refresh(user_item)
    return user_item
