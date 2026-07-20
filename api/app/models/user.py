from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    last_name = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)

    user_books = relationship('UserBook', back_populates='user')

    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'last_name': self.last_name,
            'first_name': self.first_name
        }