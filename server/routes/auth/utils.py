"""
Useful function to be used during user authentication.
"""
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from server.database.model import UserTable
from server.database.utils import Session, get_db
from server.routes.user.schemas import User

# defining oauth scheme
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

# crypt object
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # DEVELOPMENT ONLY
ALGORITHN = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# base functions
def get_hashed_user_password(password: str) -> str:
    """
    Create a hash over user password.
    """
    return pwd_context.hash(secret=password)


def verify_password(password: str, db_password: str) -> bool:
    """
    Verify if the given passowrd is correct
    or not.
    """
    return pwd_context.verify(secret=password, hash=db_password)


def get_user(db: Session, username: str) -> UserTable | None:
    """
    Return an user given its username
    if it was found.
    """
    return db.query(UserTable).filter(UserTable.username == username).first()


def authenticate_current_user(db: Session, username: str, password: str) -> UserTable:
    """
    Check if user is valid.
    """
    user = get_user(db=db, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists"
        )
    if not verify_password(password=password, db_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
        )
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create an access token when an user
    login.
    """
    # adding token expiration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # adding expiration time
    data.update({"exp": expire})
    return jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHN)


# async functions
async def get_current_user(
    token: Annotated[str, Depends(dependency=oauth_scheme)],
    db: Annotated[Session, Depends(dependency=get_db)],
) -> list[User]:
    """
    Return the current logged user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHN)
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db=db, username=username)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
    user: Annotated[User, Depends(dependency=get_current_user)]
):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user
