from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session as SessionType
from typing import List

from app.dependencies import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookOut
router = APIRouter(tags=["books"])

@router.get("/books", response_model=List[BookOut])
def get_books(db: SessionType = Depends(get_db)):
    return db.query(Book).all()

@router.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: SessionType = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
