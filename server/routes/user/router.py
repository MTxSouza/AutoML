"""
User routes to interact that allows to interact 
to database content related to them.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from automl.utils import check_file_content
from server.database.utils import (Session, delete_file_instance, get_db,
                                   insert_new_file, select_files)
from server.routes.auth.utils import get_current_active_user
from server.routes.user.schemas import File, User

# creating router
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[
        Depends(dependency=get_current_active_user),
        Depends(dependency=get_db),
    ],
)


# routes
@router.get(path="/me", response_model=User, status_code=200)
async def get_current_user(
    user: Annotated[User, Depends(dependency=get_current_active_user)]
):
    """
    Return all basic information about the
    current logged user.
    """
    return user


@router.get(path="/files", response_model=list[File], status_code=200)
async def list_files(
    user: Annotated[User, Depends(dependency=get_current_active_user)],
    db: Annotated[Session, Depends(dependency=get_db)],
):
    """
    Return all files of user.
    """
    return select_files(db=db, user_id=user.id)


@router.post(path="/upload", response_model=File, status_code=201)
async def upload_file(
    file: UploadFile,
    db: Annotated[Session, Depends(dependency=get_db)],
    user: Annotated[User, Depends(dependency=get_current_active_user)],
):
    """
    Upload the file to run the auto-ml
    system.
    """
    file_content = check_file_content(file=file)
    # adding user id
    file_content["user_id"] = user.id
    return insert_new_file(db=db, data=file_content)


@router.delete(path="/files", response_model=File, status_code=201)
async def delete_file(
    file_id: int,
    user: Annotated[User, Depends(dependency=get_current_active_user)],
    db: Annotated[Session, Depends(dependency=get_db)],
):
    """
    Delete a file of user.
    """
    return delete_file_instance(db=db, user_id=user.id, file_id=file_id)
