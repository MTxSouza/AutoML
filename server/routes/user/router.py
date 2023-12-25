"""
User routes to interact that allows to interact 
to database content related to them.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from automl.utils import check_file_content
from server.routes.auth.utils import get_current_active_user
from server.routes.user.schemas import User, UserBase

# creating router
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(dependency=get_current_active_user)],
)


# routes
@router.get(path="/me", response_model=User, status_code=200)
async def get_current_user(
    user: Annotated[UserBase, Depends(dependency=get_current_active_user)]
):
    """
    Return all basic information about the
    current logged user.
    """
    return user


@router.post(path="/upload", response_model=dict, status_code=201)
async def upload_file(
    file: UploadFile,
    user: Annotated[UserBase, Depends(dependency=get_current_active_user)],
):
    """
    Upload the file to run the auto-ml
    system.
    """
    return check_file_content(file=file)
