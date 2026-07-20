import os

from dotenv import load_dotenv


def get_database_connection_string():
    load_dotenv()
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOSTNAME")

    if not all([DB_NAME, DB_USER, DB_PASS, DB_HOST]):
        raise EnvironmentError(
            "One or more required environment variables are not set."
        )

    connection_string = (
        f"postgresql+psycopg://" f"{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )
    return connection_string
