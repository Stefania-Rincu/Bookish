from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class UserBook(Base):
    __tablename__ = 'user_book'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_book = Column(Integer, ForeignKey('Book.id'), nullable=False)
    due_return = Column(Date, nullable=False)

    user = relationship('User', back_populates='user_books')
    book = relationship('Book', back_populates='user_books')

    def __init__(self, id_user, id_book, due_return):
        self.id_user = id_user
        self.id_book = id_book
        self.due_return = due_return

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'id_user': self.id_user,
            'id_book': self.id_book,
            'due_return': self.due_return
        }