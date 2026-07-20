from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class AuthorBook(Base):
    # This sets the name of the table in the database
    __tablename__ = 'AuthorBook'
    __table_args__ = (UniqueConstraint('id_author', 'id_book', name='unique_author_book'),)

    # Here we outline what columns we want in our database
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_author = Column(Integer, ForeignKey('Author.id'), nullable=False)
    id_book = Column(Integer, ForeignKey('Book.id'), nullable=False)

    author = relationship('Author', back_populates='author_books')
    book = relationship('Book', back_populates='author_books')

    def __init__(self, id_author, id_book):
        self.id_author = id_author
        self.id_book = id_book

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'id_author': self.id_author,
            'id_book': self.id_book
        }