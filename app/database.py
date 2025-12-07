from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Load database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://devuser:devpass123@localhost:5432/ryze_dev")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your models
Base = declarative_base()

# ✅ This is the missing part
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
