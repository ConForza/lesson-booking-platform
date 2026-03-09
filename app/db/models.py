from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    instrument = Column(String, nullable=True)

class LessonDB(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String, index=True, nullable=False)
    instrument = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)