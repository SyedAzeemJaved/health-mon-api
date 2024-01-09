from fastapi import Depends, HTTPException, APIRouter

from sqlite.database import get_db
from sqlalchemy.orm import Session

import sqlite.crud.users as users

from sqlite.schemas import (
    User,
    UserUpdateClass,
    UserPasswordUpdateClass,
)

from utils.common import are_object_to_edit_and_other_object_same
from utils.auth import get_current_user
from utils.responses import common_responses

router = APIRouter(
    prefix="/common/me",
    tags=["common - me"],
    dependencies=[
        Depends(get_current_user),
    ],
    responses=common_responses(),
)


@router.get(
    "",
    summary="Get current user based on access token",
    response_model=User,
)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put(
    "",
    summary="Update current user",
    response_model=User,
)
async def update_me(
    user: UserUpdateClass,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    other_object = users.get_user_by_email(user_email=user.email, db=db)
    if other_object:
        if not are_object_to_edit_and_other_object_same(
            obj_to_edit=current_user, other_object_with_same_unique_field=other_object
        ):
            raise HTTPException(
                status_code=403, detail="User with same email already exists"
            )
    if user.additional_details.phone:
        other_object = users.get_user_by_phone(
            user_phone=user.additional_details.phone, db=db
        )
        if other_object:
            if not are_object_to_edit_and_other_object_same(
                obj_to_edit=current_user,
                other_object_with_same_unique_field=other_object,
            ):
                raise HTTPException(
                    status_code=403, detail="This phone number is already in use"
                )
    return users.update_user(user=user, db_user=current_user, db=db)


@router.patch(
    "/password",
    summary="Update current user's password",
    response_model=User,
)
async def update_my_password(
    new_password: UserPasswordUpdateClass,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return users.update_user_password(
        new_password=new_password, db_user=current_user, db=db
    )
