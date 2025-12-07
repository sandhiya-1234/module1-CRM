import pytest
from pytest_mock import session_mocker
from sqlalchemy import create_engine
from app.database import Base, SessionLocal
import os

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = session_mocker(bind=test_engine, autoflush=False, autocommit=False)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=test_engine)
