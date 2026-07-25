from datetime import datetime, timezone

from sqlalchemy.orm import Session

from db.models import User
from schemas import UserCreate
from security import get_pwd_hash, verify_pwd


def create_user(
    db: Session,
    user: UserCreate
) -> User:

    hashed_password = get_pwd_hash(
        user.password.get_secret_value()  # SecretStr
    )

    db_user = User(
        name=user.name,
        age=user.age,
        email=user.email,
        role=user.role,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_email(
    db: Session,
    email: str
) -> User | None:

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User | None:

    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not verify_pwd(
        password,
        user.hashed_password
    ):
        return None

    user.last_login_dtm = datetime.now(timezone.utc)
    db.commit()

    return user
