from sqlalchemy.orm import Session

from app.db.models import UserDB
from app.schemas.auth import User

class UserRepository:
    def get_user_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    def create_user(self, user: User):
        raise NotImplementedError

class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self.users = [
            User(
                email="staff@member.com",
                password="my_password",
                is_active=True,
            )
        ]

    def get_user_by_email(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def create_user(self, user: User):
        self.users.append(
            User(
                email=user.email,
                password=user.password,
                is_active=True,
            )
        )

class SqlAlchemyUserRepository(UserRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        row = (
            self.db.query(UserDB)
            .filter(UserDB.email == email)
            .first()
        )
        if row is None:
            return None

        return User(
            email=row.email,
            password=row.password_hash,
            is_active=row.is_active,
        )

    def create_user(self, user: User):
        db_user = UserDB(
            email=user.email,
            password_hash=user.password,
            is_active=user.is_active,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
