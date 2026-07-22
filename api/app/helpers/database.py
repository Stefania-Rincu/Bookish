from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.helpers.database_connection_string import get_database_connection_string

# Database Url to connect to.
# recommend to create an environment variable and read the url from it.
DATABASE_URL = get_database_connection_string()

# engine object that connects to the alembic specified.
engine = create_engine(DATABASE_URL)

# create new session which is bound to the engine object created earlier.
# autocommit and autoflush false means
# not to make changes in alembic when there's
# change in session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for table_models which contains necessary functionality to
# interact with alembic using ORM.
Base = declarative_base()
