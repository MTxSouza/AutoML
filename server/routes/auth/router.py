"""
Authentication route to login an user.
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from server.database.model import UserTable
from server.database.utils import Session, get_db, insert_new_instance
from server.routes.auth.schemas import Token
from server.routes.auth.utils import (authenticate_current_user,
                                      create_access_token,
                                      get_hashed_user_password)
from server.routes.user.schemas import User, UserCreate, UserInDB

# creating router
router = APIRouter(tags=["Auth"])


# routes
@router.post(path="/token", response_model=Token, status_code=201)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(dependency=get_db),
):
    """
    Login an user.
    """
    # authenticating user
    user = authenticate_current_user(
        db=db, username=form_data.username, password=form_data.password
    )
    # creating token access
    token_access = create_access_token(data={"sub": user.username})
    return {"access_token": token_access, "token_type": "bearer"}


@router.post(path="/register", response_model=User, status_code=201)
async def register_new_user(user: UserCreate, db: Session = Depends(dependency=get_db)):
    """
    Register a new user to the database.
    """
    # hashing password
    hashed_password = get_hashed_user_password(
        password=user.password.get_secret_value()
    )
    return insert_new_instance(
        db=db,
        table=UserTable,
        data=UserInDB.model_construct(
            username=user.username, hashed_password=hashed_password
        ),
    )
