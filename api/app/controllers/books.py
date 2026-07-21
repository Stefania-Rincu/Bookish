from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session as SessionType
from typing import List

from app.dependencies import get_db
from app.models.author import Author
from app.models.author_book import AuthorBook
from app.models.book import Book
from app.schemas.book import BookCreate, BookOut
router = APIRouter(tags=["books"])

@router.get("/books", response_model=List[BookOut])
def get_books(db: SessionType = Depends(get_db)):
    return db.query(Book).all()

@router.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: SessionType = Depends(get_db)):
    db_book = Book(title=book.title, isbn=book.isbn, num_copies=book.num_copies)
    db.add(db_book)
    db.flush()

    for author_name in book.authors:
        author = db.query(Author).filter(
            func.lower(Author.author_name) == author_name.lower()
        ).first()
        if not author:
            author = Author(author_name=author_name)
            db.add(author)
            db.flush()
        db.add(AuthorBook(id_author=author.id, id_book=db_book.id))

    db.commit()
    db.refresh(db_book)
    return db_book
