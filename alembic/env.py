from dotenv import load_dotenv
import sys
import os
load_dotenv()

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic config
config = context.config

# Load DATABASE_URL from .env if present
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
if "downgrade" in sys.argv and os.getenv("ALLOW_DOWNGRADE") != "1":
    raise RuntimeError(
        "Alembic downgrades are disabled. Set ALLOW_DOWNGRADE=1 to enable (use with caution)."
    )

# Import models so Alembic can see them
from app.database import Base
from app import models  # 👈 this ensures Lead, Deal are registered

# Set metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
