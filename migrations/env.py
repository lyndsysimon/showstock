from logging.config import fileConfig

from alembic import context

# Import the SQLAlchemy Base and models
from showstock.db import Base

# Import models to ensure they're registered with Base
import showstock.models  # noqa
from showstock.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the SQLAlchemy URL in the Alembic config
config.set_main_option("sqlalchemy.url", str(settings.db.DATABASE_URL))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Create migration without connecting to database.
    # Useful when no database connection is available.
    # In production, use the commented-out code below.

    # Configure Alembic to use our metadata directly without a connection
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Include these options for better migrations
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()

    # Original code for when database connection is available:
    """
    # For async SQLAlchemy, we need to get a sync engine for Alembic
    # Extract the connection URL from the config
    configuration = config.get_section(config.config_ini_section)

    # Replace the async driver with a sync one for Alembic
    url = configuration["sqlalchemy.url"]
    url = url.replace("postgresql+asyncpg", "postgresql")

    # Import here to avoid unused import errors
    from sqlalchemy import engine_from_config, pool

    # Create a sync engine for Alembic
    connectable = engine_from_config(
        {"sqlalchemy.url": url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Include these options for better migrations
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()
    """


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
