from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserUpdate


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(db: Session, user: UserCreate) -> User:

    db_user = User(**user.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate
) -> User | None:
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(
    db: Session,
    user_id: int
) -> User | None:
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user
