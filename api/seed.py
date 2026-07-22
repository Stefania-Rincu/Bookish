from datetime import date
from sqlalchemy import text
from app.helpers.database import Session
from app.models.author import Author
from app.models.book import Book
from app.models.author_book import AuthorBook
from app.models.user import User
from app.models.user_book import UserBook
from app.services.auth import get_password_hash

session = Session()

# Wipe existing data and reset IDs so the seed script can be run multiple times.
session.execute(text('TRUNCATE TABLE user_books, author_books, users, books, authors RESTART IDENTITY CASCADE'))
session.commit()

book_1 = Book(title="Harry Potter and the Philosopher's Stone", isbn='9780747532743', num_copies=4)
book_2 = Book(title='Harry Potter and the Chamber of Secrets', isbn='9781408855669', num_copies=2)
book_3 = Book(title='How Technology Is Changing Human Behavior', isbn='9781440869518', num_copies=3)
book_4 = Book(title='Forms that Work: Designing Web Forms for Usability', isbn='9781558607101', num_copies=4)
book_5 = Book(title="Don't Make Me Think, Revisited", isbn='9780321965516', num_copies=2)

author_1 = Author(author_name='J K Rowling')
author_2 = Author(author_name='Rossana Pasquino')
author_3 = Author(author_name='C.G. Prado')
author_4 = Author(author_name='Caroline Jarrett')
author_5 = Author(author_name='Gerry Gaffney')
author_6 = Author(author_name='Steve Krug')

user_1 = User('Doe', 'Jane', 'jane_doe', get_password_hash('jane123'))
user_2 = User('Something', 'Joe', 'joe_something', get_password_hash('joe123'))
user_3 = User('Somethingelse', 'John', 'john_somethingelse', get_password_hash('john123'))
user_4 = User('Sparrow', 'Jack', 'jack_sparrow', get_password_hash('jack123'))

session.add_all([book_1, book_2, book_3, book_4, book_5, author_1, author_2, author_3, author_4, author_5, author_6, user_1, user_2, user_3, user_4])
session.flush()

session.add_all([
    AuthorBook(id_author=author_1.id, id_book=book_1.id),
    AuthorBook(id_author=author_1.id, id_book=book_2.id),
    AuthorBook(id_author=author_2.id, id_book=book_3.id),
    AuthorBook(id_author=author_3.id, id_book=book_3.id),
    AuthorBook(id_author=author_4.id, id_book=book_4.id),
    AuthorBook(id_author=author_5.id, id_book=book_4.id),
    AuthorBook(id_author=author_6.id, id_book=book_5.id),
])

session.add_all([
    UserBook(id_user=user_1.id, id_book=book_1.id, due_return=date(2026, 7, 3)),
    UserBook(id_user=user_1.id, id_book=book_2.id, due_return=date(2026, 7, 3)),
    UserBook(id_user=user_1.id, id_book=book_3.id, due_return=date(2026, 7, 25)),
    UserBook(id_user=user_1.id, id_book=book_4.id, due_return=date(2026, 7, 25)),
    UserBook(id_user=user_2.id, id_book=book_1.id, due_return=date(2026, 7, 22)),
    UserBook(id_user=user_2.id, id_book=book_3.id, due_return=date(2026, 7, 13)),
    UserBook(id_user=user_3.id, id_book=book_3.id, due_return=date(2026, 7, 25)),
    UserBook(id_user=user_3.id, id_book=book_4.id, due_return=date(2026, 7, 15)),
    UserBook(id_user=user_4.id, id_book=book_4.id, due_return=date(2026, 7, 30)),
])

session.commit()
