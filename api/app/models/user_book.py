from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class UserBook(Base):
    __tablename__ = 'user_books'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_book = Column(Integer, ForeignKey('books.id'), nullable=False)
    due_return = Column(Date, nullable=False)
    returned_date = Column(Date, nullable=True)

    user = relationship('User', back_populates='user_books')
    book = relationship('Book', back_populates='user_books')

    def __init__(self, id_user, id_book, due_return, returned_date=None):
        self.id_user = id_user
        self.id_book = id_book
        self.due_return = due_return
        self.returned_date = returned_date
