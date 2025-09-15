from dotenv import load_dotenv
import os
load_dotenv()

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic Config object
config = context.config

# Load .env DATABASE_URL into Alembic
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import metadata
from app.database import Base
target_metadata = Base.metadata
