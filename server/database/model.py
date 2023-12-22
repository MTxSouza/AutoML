"""
Database table models to be used to structure
and organize any data into database.
"""
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.exc import OperationalError

from server.database.config import ENGINE, Base


class UserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    username = Column(String(length=40), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, nullable=False)
    photo = Column(String, nullable=True)


# creating tables
try:
    Base.metadata.create_all(ENGINE)
except OperationalError as error:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
