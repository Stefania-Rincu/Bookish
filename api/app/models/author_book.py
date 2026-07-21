from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class AuthorBook(Base):
    __tablename__ = 'author_books'
    __table_args__ = (UniqueConstraint('id_author', 'id_book', name='unique_author_book'),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_author = Column(Integer, ForeignKey('authors.id'), nullable=False)
    id_book = Column(Integer, ForeignKey('books.id'), nullable=False)

    author = relationship('Author', back_populates='author_books')
    book = relationship('Book', back_populates='author_books')

    def __init__(self, id_author, id_book):
        self.id_author = id_author
        self.id_book = id_book
