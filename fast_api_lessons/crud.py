from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_email(db: Session, email: str):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(db: Session, user: UserCreate):

    db_user = User(**user.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(
    db: Session,
    user_id: int,
    user_data: UserCreate
):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    for field, value in user_data.model_dump().items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(
    db: Session,
    user_id: int
):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user
