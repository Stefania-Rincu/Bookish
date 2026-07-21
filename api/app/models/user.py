from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint('username', name='unique_username'),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    last_name = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    username = Column(String(30), nullable=False)
    password_hash = Column(String(256), nullable=False)

    user_books = relationship('UserBook', back_populates='user')

    def __init__(self, last_name, first_name, username, password_hash):
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.password_hash = password_hash
