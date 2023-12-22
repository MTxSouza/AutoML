"""
Useful functions to be used to interact to
database.
"""
from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from server.database.config import Session
from server.database.model import Base


def get_db():
    """
    Return a database object.
    """
    try:
        db = Session()
        yield db
    finally:
        db.close()


# SELECT
def select_instances(db: Session, table: Base, skip: int, limit: int) -> list[Base]:
    """
    Select N instances from any table
    from database.
    """
    return db.query(table).offset(skip).limit(limit).all()


# INSERT
def insert_new_instance(db: Session, table: Base, data: BaseModel | dict) -> Base:
    """
    Insert a new instance into any table
    in database.
    """
    if isinstance(data, BaseModel):
        data = data.model_dump()
    db_instace = table(**data)
    db.add(db_instace)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    db.refresh(db_instace)
    return db_instace
