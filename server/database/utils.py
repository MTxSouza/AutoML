"""
Useful functions to be used to interact to
database.
"""
from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from server.database.config import Session
from server.database.model import Base, FileTable, UserTable
from server.logging import logger


def get_db():
    """
    Return a database object.
    """
    logger.debug(msg="get_db() has been called")
    try:
        db = Session()
        yield db
    finally:
        db.close()


# SELECT
def select_instances(db: Session, table: Base, skip: int, limit: int) -> list[Base]:
    """
    Select N instances from any table
    in database.
    """
    logger.trace(msg="select_instances() has been called")
    return db.query(table).offset(skip).limit(limit).all()


def select_one_instance(db: Session, table: Base, instance_id: int) -> Base | None:
    """
    Select one instance from any table
    in database.
    """
    logger.trace(msg="select_one_instance() has been called")
    return db.query(table).filter(table.id == instance_id).first()


def select_files(db: Session, user_id: int) -> list[Base]:
    """
    Select N files registered by user.
    """
    logger.trace(msg="select_files() has been called")
    return db.query(FileTable).filter(FileTable.user_id == user_id).all()


# INSERT
def insert_new_instance(db: Session, table: Base, data: BaseModel | dict) -> Base:
    """
    Insert a new instance into any table
    in database.
    """
    logger.trace(msg="insert_new_instance() has been called")
    if isinstance(data, BaseModel):
        data = data.model_dump()
    db_instace = table(**data)
    db.add(db_instace)
    db.commit()
    db.refresh(db_instace)
    return db_instace


def insert_new_user(db: Session, data: dict) -> Base:
    """
    Insert a new user to database.
    """
    logger.trace(msg="insert_new_user() has been called")
    try:
        return insert_new_instance(db=db, table=UserTable, data=data)
    except IntegrityError:
        logger.error(msg=f"Username {data['username']} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )


def insert_new_file(db: Session, data: dict) -> Base:
    """
    Insert a new user to database.
    """
    logger.trace(msg="insert_new_file() has been called")
    try:
        return insert_new_instance(db=db, table=FileTable, data=data)
    except IntegrityError:
        logger.error(msg=f"This file already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File already exists"
        )


# DELETE
def delete_instance(db: Session, table: Base, instance_id: int) -> Base | None:
    """
    Delete an instance from any table
    in database.
    """
    logger.trace(msg="delete_instance() has been called")
    instance = select_one_instance(db=db, table=table, instance_id=instance_id)
    if instance:
        db.delete(instance)
        db.commit()
    return instance
