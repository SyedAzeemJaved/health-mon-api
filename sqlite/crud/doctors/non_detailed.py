from sqlalchemy import func
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
        .options(joinedload(models.UserModel.additional_details))
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.DOCTOR,
                models.UserModel.id.in_(doctor_ids),
            )
        )
    )


def get_doctor_by_id(user_id: int, db: Session):
    """Get a single doctor by id from the database"""
    return (
        db.query(models.UserModel)
        .options(joinedload(models.UserModel.additional_details))
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.DOCTOR,
                models.UserModel.id == user_id,
            )
        )
        .first()
    )


def get_all_doctor_ids_for_a_particular_patient(user_id: int, db: Session):
    """Get all doctor ids for a particular patient from the database"""
    return (
        db.query(
            func.group_concat(
                func.distinct(models.patient_doctor_association_table.c.doctor_id)
            )
        )
        .filter(models.patient_doctor_association_table.c.patient_id == user_id)
        .first()
    )
