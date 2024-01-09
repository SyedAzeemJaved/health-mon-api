from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlite.database import get_db
from sqlalchemy.orm import Session

from typing import Annotated
from jose import JWTError, jwt

from secret import secret

from sqlite.models import UserModel

from sqlite.schemas import TokenData
from sqlite.enums import UserRoleEnum, CombinedRoleEnum

import sqlite.crud.users as users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    """Get current user, based on the access token that they provided"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret.SECRET_KEY, algorithms=[secret.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = users.get_user_by_email(user_email=token_data.email, db=db)
    if user is None:
        raise credentials_exception
    return user


async def user_should_be_admin(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if current_user.user_role == CombinedRoleEnum.ADMIN:
        return current_user
    raise HTTPException(
        status_code=400,
        detail="You do not have the necessary permission to access this route",
    )


async def user_should_not_be_admin(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if current_user.user_role != CombinedRoleEnum.ADMIN:
        return current_user
    raise HTTPException(
        status_code=400,
        detail="Admins can not access this route",
    )


async def user_should_be_patient(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if current_user.user_role == UserRoleEnum.PATIENT:
        return current_user
    raise HTTPException(
        status_code=400,
        detail="You do not have the necessary permission to access this route",
    )
