from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from sqlite import models

from sqlite.enums import UserRoleEnum


def get_all_patients_by_list_of_ids(
    patient_ids: list[int], db: Session
) -> list[models.UserModel]:
    """Get all patients by list of ids from the database"""
    return (
        db.query(models.UserModel)
        .options(joinedload(models.UserModel.additional_details))
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.PATIENT,
                models.UserModel.id.in_(patient_ids),
            )
        )
    )


def get_patient_by_id(user_id: int, db: Session) -> models.UserModel:
    """Get a single patient by id from the database"""
    return (
        db.query(models.UserModel)
        .options(joinedload(models.UserModel.additional_details))
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.PATIENT,
                models.UserModel.id == user_id,
            )
        )
        .first()
    )
