from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from sqlite import models

from sqlite.enums import UserRoleEnum


def get_all_caretakers_by_list_of_ids(
    caretaker_ids: list[int], db: Session
) -> list[models.UserModel]:
    """Get all caretakers by list of ids from the database"""
    return (
        db.query(models.UserModel)
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.CARETAKER,
                models.UserModel.id.in_(caretaker_ids),
            )
        )
        .options(joinedload(models.UserModel.additional_details))
    )


def get_caretaker_by_id(user_id: int, db: Session) -> models.UserModel:
    """Get a single caretaker by id from the database"""
    return (
        db.query(models.UserModel)
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.CARETAKER,
                models.UserModel.id == user_id,
            )
        )
        .options(joinedload(models.UserModel.additional_details))
        .first()
    )
