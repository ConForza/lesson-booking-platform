import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
import app.core.deps as deps
from app.db.database import Base
from app.db.models import StudentDB, LessonDB

TEST_DB_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_database():
    app.dependency_overrides[deps.get_db] = override_get_db

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        db.add(
            StudentDB(
                student_email="joe@bloggs.com",
                first_name="Joe",
                surname="Bloggs",
                instrument="piano",
            )
        )
        db.add(
            StudentDB(
                student_email="some@person.com",
                first_name="Some",
                surname="Person",
                instrument="violin",
            )
        )
        db.add(
            LessonDB(
                student_email="joe@bloggs.com",
                instrument="piano",
                datetime=datetime(2026, 1, 6, 12, 30),
                duration=30,
            )
        )
        db.add(
            LessonDB(
                student_email="joe@bloggs.com",
                instrument="piano",
                datetime=datetime(2026, 1, 15, 17, 0),
                duration=60,
            )
        )
        db.add(
            LessonDB(
                student_email="joe@bloggs.com",
                instrument="piano",
                datetime=datetime(2026, 2, 23, 19, 30),
                duration=30,
            )
        )
        db.add(
            LessonDB(
                student_email="some@person.com",
                instrument="violin",
                datetime=datetime(2026, 1, 28, 18, 30),
                duration=30,
            )
        )
        db.commit()
    finally:
        db.close()

    yield
    app.dependency_overrides.clear()

@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client():
    return TestClient(app)
