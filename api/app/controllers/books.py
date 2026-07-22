from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionType, joinedload, selectinload
from typing import List
from app.dependencies import get_current_user, get_db
from app.models.author import Author
from app.models.author_book import AuthorBook
from app.models.book import Book
from app.models.user import User
from app.models.user_book import UserBook
from app.schemas.book import BookCreate, BookOut, CheckedOutBook
router = APIRouter(tags=["books"])

@router.get("/books", response_model=List[BookOut])
def get_books(db: SessionType = Depends(get_db)):
    return db.query(Book).all()

@router.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: SessionType = Depends(get_db)):
    authors = [a.strip() for a in book.authors]
    if not authors or any(not author for author in authors):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Books must have at least one author",
        )

    try:
        db_book = Book(title=book.title, isbn=book.isbn, num_copies=book.num_copies)
        db.add(db_book)
        db.flush()

        for author_name in authors:
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
    except IntegrityError as exc:
        db.rollback()
        error_msg = str(exc.orig)
        if "unique_isbn" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A book with this ISBN already exists",
            )
        if "ck_num_copies" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Number of copies must be greater than 0",
            )
        if "unique_author_book" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Author is already linked to this book",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error",
        )

@router.get("/books/checked-out", response_model=List[CheckedOutBook])
def get_checked_out_books(
    current_user: User = Depends(get_current_user),
    db: SessionType = Depends(get_db)
):
    user_books = (
        db.query(UserBook)
        .options(
            joinedload(UserBook.book)
            .selectinload(Book.author_books)
            .selectinload(AuthorBook.author)
        )
        .filter(
            UserBook.id_user == current_user.id,
            UserBook.returned_date.is_(None),
        )
        .all()
    )
    return [
        {
            "id": user_book.book.id,
            "title": user_book.book.title,
            "isbn": user_book.book.isbn,
            "due_return": user_book.due_return,
            "authors": [ab.author.author_name for ab in user_book.book.author_books],
        }
        for user_book in user_books
    ]
