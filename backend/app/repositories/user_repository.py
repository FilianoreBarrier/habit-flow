
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[User]:
        stmt = select(User).options(selectinload(User.habits))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self,user_id:int) -> User | None:
        return self.db.get(User, user_id)
    
    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))
    
    def get_by_username(self, username: str) -> User | None:
        return self.db.scalar(select(User).where(User.username == username))
                              
    def create(self, user_data: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username = user_data.username,
            email = user_data.email,
            full_name =user_data.full_name,
            hashed_password = hashed_password,
            is_active = True
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    def get_multiple_by_ids(self, user_ids: list[int])-> list[User]:
        stmt = select(User).where(User.user_id.in_(user_ids))
        return list(self.db.scalars(stmt).all())
