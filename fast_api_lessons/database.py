from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False  # prevents SQLAlchemy from expiring ORM objects after commit()
)

def get_db() -> Generator[Session, None, None]:  # [yields Session, receives nothing via "send()", returns nothing]
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
