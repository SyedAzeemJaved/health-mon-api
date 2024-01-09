from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from sqlite import models

from sqlite.enums import UserRoleEnum


def get_all_doctors_by_list_of_ids(
    doctor_ids: list[int], db: Session
) -> list[models.UserModel]:
    """Get all doctors by list of ids from the database"""
    return (
        db.query(models.UserModel)
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.DOCTOR,
                models.UserModel.id.in_(doctor_ids),
            )
        )
        .options(joinedload(models.UserModel.additional_details))
    )


def get_doctor_by_id(user_id: int, db: Session) -> models.UserModel:
    """Get a single doctor by id from the database"""
    return (
        db.query(models.UserModel)
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.DOCTOR,
                models.UserModel.id == user_id,
            )
        )
        .options(joinedload(models.UserModel.additional_details))
        .first()
    )
