# Database Models

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Enum as SqlEnum

from constants import LoanStatus


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    role = Column(String(100), nullable=True)
    
    loans = relationship("Loan", back_populates="user")

    created_dtm = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_dtm = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_dtm = Column(DateTime(timezone=True), nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    interest_rate = Column(Integer, nullable=False)
    created_dtm = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_dtm = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(SqlEnum(LoanStatus))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="loans")
