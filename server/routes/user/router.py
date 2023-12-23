"""
User routes to interact that allows to interact 
to database content related to them.
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from server.database.model import UserTable
from server.routes.auth.utils import get_current_user
from server.routes.user.schemas import User, UserBase

# creating router
router = APIRouter(prefix="/users", tags=["Users"])


# routes
@router.get(path="/me", response_model=User, status_code=200)
async def get_current_user(
    user: Annotated[UserBase, Depends(dependency=get_current_user)]
):
    """
    Return all basic information about the
    current logged user.
    """
    ...
