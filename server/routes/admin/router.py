"""
User routes to interact that allows to interact 
to database content related to them.
"""
from fastapi import APIRouter, Depends

from server.database.model import UserTable
from server.database.utils import Session, get_db, select_instances
from server.routes.user.schemas import User

# creating router
router = APIRouter(prefix="/admin", tags=["Admin"])


# routes
@router.get(path="/", response_model=list[User], status_code=200)
async def get_users(
    limit: int = -1, skip: int = 0, db: Session = Depends(dependency=get_db)
):
    """
    Return all users from database.
    """
    return select_instances(db=db, table=UserTable, skip=skip, limit=limit)
