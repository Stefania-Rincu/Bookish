from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionType, joinedload, selectinload
from typing import List
from app.dependencies import get_current_user, get_db
from app.models.author import Author
from app.models.author_book import AuthorBook
from app.models.book import Book
from app.models.user import User
from app.models.user_book import UserBook
from app.schemas.book import BookAvailability, BookCreate, BookOut, CheckedOutBook, PagedBooks
from app.schemas.user_book import Borrower
router = APIRouter(tags=["books"])

@router.get("/books", response_model=PagedBooks)
def get_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: SessionType = Depends(get_db),
):
    total = db.query(Book).count()
    items = (
        db.query(Book)
        .options(selectinload(Book.author_books).selectinload(AuthorBook.author))
        .order_by(Book.title.asc(), Book.id.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return PagedBooks(
        items=[
            BookOut(
                id=book.id,
                title=book.title,
                isbn=book.isbn,
                num_copies=book.num_copies,
                authors=[ab.author.author_name for ab in book.author_books],
            )
            for book in items
        ],
        total=total,
        page=page,
        page_size=page_size,
    )

@router.get("/books/search", response_model=List[BookOut])
def search_books(
    q: str = Query(..., min_length=1),
    db: SessionType = Depends(get_db),
):
    pattern = f"%{q.strip()}%"
    books = (
        db.query(Book)
        .outerjoin(AuthorBook, AuthorBook.id_book == Book.id)
        .outerjoin(Author, Author.id == AuthorBook.id_author)
        .filter(or_(Book.title.ilike(pattern), Author.author_name.ilike(pattern)))
        .distinct()
        .options(selectinload(Book.author_books).selectinload(AuthorBook.author))
        .order_by(Book.title.asc(), Book.id.asc())
        .all()
    )
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No book found",
        )
    return [
        BookOut(
            id=book.id,
            title=book.title,
            isbn=book.isbn,
            num_copies=book.num_copies,
            authors=[ab.author.author_name for ab in book.author_books],
        )
        for book in books
    ]

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
        return BookOut(
            id=db_book.id,
            title=db_book.title,
            isbn=db_book.isbn,
            num_copies=db_book.num_copies,
            authors=authors,
        )
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

@router.get("/books/{book_id}/availability", response_model=BookAvailability)
def get_book_availability(book_id: int, db: SessionType = Depends(get_db)):
    book = (
        db.query(Book)
        .options(selectinload(Book.author_books).selectinload(AuthorBook.author))
        .filter(Book.id == book_id)
        .first()
    )
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    active_loans = (
        db.query(UserBook)
        .options(joinedload(UserBook.user))
        .filter(
            UserBook.id_book == book_id,
            UserBook.returned_date.is_(None),
        )
        .all()
    )
    return BookAvailability(
        id=book.id,
        title=book.title,
        isbn=book.isbn,
        num_copies=book.num_copies,
        authors=[ab.author.author_name for ab in book.author_books],
        available_copies=book.num_copies - len(active_loans),
        borrowers=[
            Borrower(
                name=f"{loan.user.first_name} {loan.user.last_name}",
                due_return=loan.due_return,
            )
            for loan in active_loans
        ],
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
        CheckedOutBook(
            id=user_book.book.id,
            title=user_book.book.title,
            isbn=user_book.book.isbn,
            num_copies=user_book.book.num_copies,
            due_return=user_book.due_return,
            authors=[ab.author.author_name for ab in user_book.book.author_books],
        )
        for user_book in user_books
    ]
