"""
Schemas related to user.
"""
from typing import Optional

from pydantic import BaseModel, SecretStr


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: SecretStr

    model_config = {
        "json_schema_extra": {"examples": [{"username": "admin", "password": "admin"}]}
    }


class User(UserBase):
    id: Optional[int]
    disabled: bool = False
    photo: str | None = None

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str


class File(BaseModel):
    id: Optional[int]
    filename: str
    separator: str
    file: str
    encoding: str
    size: int

    class Config:
        from_attributes = True
