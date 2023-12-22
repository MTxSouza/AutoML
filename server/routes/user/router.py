"""
User routes to interact that allows to interact 
to database content related to them.
"""
from typing import Annotated

from app.database.model import UserTable
from app.routes.auth.utils import get_current_user
from app.routes.user.schemas import User, UserBase
from fastapi import APIRouter, Depends

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
