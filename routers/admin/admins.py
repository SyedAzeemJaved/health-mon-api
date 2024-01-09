from fastapi import Depends, HTTPException, APIRouter

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlite.database import get_db
from sqlalchemy.orm import Session

import sqlite.crud.admins as crud

from sqlite.schemas import User

from utils.auth import user_should_be_admin
from utils.responses import common_responses

router = APIRouter(
    prefix="/admins",
    tags=["admin - admins"],
    dependencies=[
        Depends(user_should_be_admin),
    ],
    responses=common_responses(),
)


@router.get(
    "",
    summary="Get a list of all admins",
    response_model=Page[User],
)
async def get_all_admins(db: Session = Depends(get_db)):
    return paginate(crud.get_all_admins(db=db))


@router.get(
    "/{user_id}",
    summary="Get a single admin by id",
    response_model=User,
)
async def get_admin_by_id(user_id: int, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_id(user_id=user_id, db=db)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin
