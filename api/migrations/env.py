from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from typing import Any

from app.helpers.database import Base
from app.helpers.database_connection_string import get_database_connection_string
from app.models import Book, Author, AuthorBook, User, UserBook


def run_migrations_offline(context: Any, config: Any, target_metadata: Any):
    pass

def run_migrations_online(context: Any, config: Any, target_metadata: Any):
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", get_database_connection_string())


if context.is_offline_mode():
    run_migrations_offline(context=context, config=config, target_metadata=target_metadata)
else:
    run_migrations_online(context=context, config=config, target_metadata=target_metadata)