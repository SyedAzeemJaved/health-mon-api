from sqlalchemy import func
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


def get_caretaker_by_id(user_id: int, db: Session):
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


def get_all_caretaker_ids_for_a_particular_patient(user_id: int, db: Session):
    """Get all caretaker ids for a particular patient from the database"""
    return (
        db.query(
            func.group_concat(
                func.distinct(models.patient_caretaker_association_table.c.caretaker_id)
            )
        )
        .filter(models.patient_caretaker_association_table.c.patient_id == user_id)
        .first()
    )
