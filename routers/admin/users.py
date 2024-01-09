from fastapi import Depends, HTTPException, APIRouter

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlite.database import get_db
from sqlalchemy.orm import Session

import sqlite.crud.users as crud

from sqlite.schemas import (
    User,
    UserCreateClass,
    UserUpdateClass,
    UserPasswordUpdateClass,
    CommonResponseClass,
)

from utils.common import are_object_to_edit_and_other_object_same

from utils.auth import user_should_be_admin
from utils.responses import common_responses

router = APIRouter(
    prefix="/users",
    tags=["admin - users"],
    dependencies=[
        Depends(user_should_be_admin),
    ],
    responses=common_responses(),
)


@router.get(
    "",
    summary="Get all users",
    response_model=Page[User],
)
async def get_users(db: Session = Depends(get_db)):
    return paginate(crud.get_all_users(db=db))


@router.get(
    "/{user_id}",
    summary="Get a single user by id",
    response_model=User,
)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post(
    "",
    summary="Create a new user",
    response_model=User,
)
async def create_user(user: UserCreateClass, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(user_email=user.email, db=db)
    if db_user is None:
        return crud.create_user_with_additional_details(user=user, db=db)
    raise HTTPException(status_code=403, detail="User already exists")


@router.put(
    "/{user_id}",
    summary="Update an existing user",
    response_model=User,
)
async def update_user(
    user_id: int, user: UserUpdateClass, db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    other_object = crud.get_user_by_email(user_email=user.email, db=db)
    if other_object:
        if not are_object_to_edit_and_other_object_same(
            obj_to_edit=db_user, other_object_with_same_unique_field=other_object
        ):
            raise HTTPException(
                status_code=403, detail="User with same email already exists"
            )
    if user.additional_details.phone:
        other_object = crud.get_user_by_phone(
            user_phone=user.additional_details.phone, db=db
        )
        if other_object:
            if not are_object_to_edit_and_other_object_same(
                obj_to_edit=db_user, other_object_with_same_unique_field=other_object
            ):
                raise HTTPException(
                    status_code=403, detail="This phone number is already in use"
                )
    return crud.update_user(user=user, db_user=db_user, db=db)


@router.patch(
    "/password/{user_id}",
    summary="Update an existing user's password",
    response_model=User,
)
async def update_user_password(
    user_id: int,
    new_password: UserPasswordUpdateClass,
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user_password(new_password=new_password, db_user=db_user, db=db)


@router.delete(
    "/{user_id}",
    summary="Delete an existing user",
    response_model=CommonResponseClass,
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db_user=db_user, db=db)
