from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class Author(Base):
    # This sets the name of the table in the database
    __tablename__ = 'Author'

    # Here we outline what columns we want in our database
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    author_name = Column(String(50), nullable=False)

    author_books = relationship('AuthorBook', back_populates='author')

    def __init__(self, author_name):
        self.author_name = author_name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'author_name': self.author_name
        }