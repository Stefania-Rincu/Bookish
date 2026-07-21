import os

from dotenv import load_dotenv


def get_database_connection_string():
    load_dotenv()
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASS = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST")

    if not all([DB_NAME, DB_USER, DB_PASS, DB_HOST]):
        raise EnvironmentError(
            "One or more required environment variables are not set."
        )

    connection_string = (
        f"postgresql+psycopg://" f"{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )
    return connection_string
