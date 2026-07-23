# API Models

from pydantic import BaseModel, EmailStr, PositiveInt, Field


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: PositiveInt
    role: str = Field(min_length=2, max_length=100)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int  # will match Id from Db

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    age: PositiveInt | None = None
    role: str | None = Field(default=None, min_length=2, max_length=100)
