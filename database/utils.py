"""
Useful function to interact to MongoDB Server.
"""
from pymongo.database import Database

from database.config import db
from database.logging import logger as db_logger


def get_db() -> Database:
    """
    Return the MongoDB object.
    """
    db_logger.debug(msg="`get_db()` has been called. Retrieving database object")
    return db


def get_all_users(db: Database, skip: int, limit: int) -> list:
    """
    Return all users from database.
    """
    db_logger.debug(
        msg="`get_all_users()` has been called. Retrieving all users from database."
    )
    return db.get_collection(name="users").find().skip(skip=skip).to_list(length=limit)
