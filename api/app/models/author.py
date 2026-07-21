from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    author_name = Column(String(50), nullable=False)

    author_books = relationship('AuthorBook', back_populates='author')

    def __init__(self, author_name):
        self.author_name = author_name
