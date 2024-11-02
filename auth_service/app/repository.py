from sqlalchemy.orm import Session
from app.model import User, Log
from app.schema import TokenData, UserCreate


def get_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> TokenData:
    new_user = User(
        username=user.username,
        email=user.email,
        birthday=user.birthday,
        user_type=user.user_type,
        hashed_password=user.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_log(db: Session, event: str, username: str, timestamp: float):
    new_log = Log(event=event, username=username, timestamp=timestamp)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log
