from sqlalchemy import Column, Integer, String, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class Book(Base):
    __tablename__ = 'books'
    __table_args__ = (
        CheckConstraint('num_copies > 0', name='ck_num_copies'),
        UniqueConstraint('isbn', name='unique_isbn')
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False, index=True)
    isbn = Column(String(13), nullable=False)
    num_copies = Column(Integer, nullable=False)

    author_books = relationship('AuthorBook', back_populates='book')
    user_books = relationship('UserBook', back_populates='book')

    def __init__(self, title, isbn, num_copies):
        self.title = title
        self.isbn = isbn
        self.num_copies = num_copies
