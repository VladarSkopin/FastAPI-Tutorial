# API Models

from pydantic import BaseModel, EmailStr, PositiveInt, Field, SecretStr


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: PositiveInt
    role: str = Field(min_length=2, max_length=100)


class UserCreate(UserBase):
    password: SecretStr


class UserResponse(UserBase):
    id: int  # will match Id from Db
    is_active: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    age: PositiveInt | None = None
    role: str | None = Field(default=None, min_length=2, max_length=100)


# API Models for Authentication


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None
