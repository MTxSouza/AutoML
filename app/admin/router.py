"""
Routes related to admin control.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, status
from pymongo.database import Database

from app.logging import logger as api_logger
from database.utils import get_all_users, get_db

router = APIRouter(
    prefix="/admin", tags=["Admin"], dependencies=[Depends(dependency=get_db)]
)


@router.get(path="/users", status_code=status.HTTP_200_OK)
async def retrieve_users(
    db: Annotated[Database, Depends(dependency=get_db)], skip: int = 0, limit: int = 100
):
    api_logger.debug(msg="/users has been called")
    users = await get_all_users(db=db, skip=skip, limit=limit)
    return users
