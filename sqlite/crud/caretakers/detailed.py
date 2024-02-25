from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from sqlite import models

from sqlite.enums import UserRoleEnum


def get_all_caretakers_with_patients(
    db: Session,
) -> list[tuple[models.UserModel | None, str | None]]:
    """Get all caretakers with patients from the database"""
    return (
        db.query(
            models.UserModel,
            func.group_concat(
                func.distinct(models.patient_caretaker_association_table.c.patient_id)
            ).label("patient_ids"),
        )
        .outerjoin(
            models.patient_caretaker_association_table,
            models.patient_caretaker_association_table.c.caretaker_id
            == models.UserModel.id,
        )
        .options(joinedload(models.UserModel.additional_details))
        .filter(models.UserModel.user_role == UserRoleEnum.CARETAKER)
        .group_by(models.UserModel.id)
    )


def get_all_caretakers_with_patients_for_a_particular_user(
    user_id: int,
    db: Session,
) -> list[tuple[models.UserModel | None, str | None]]:
    """Get all caretakers with patients for a particular user from the database"""
    return (
        db.query(
            models.UserModel,
            func.group_concat(
                func.distinct(models.patient_caretaker_association_table.c.patient_id)
            ).label("patient_ids"),
        )
        .outerjoin(
            models.patient_caretaker_association_table,
            models.patient_caretaker_association_table.c.caretaker_id
            == models.UserModel.id,
        )
        .options(
            joinedload(models.UserModel.additional_details),
        )
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.CARETAKER,
                models.UserModel.id == user_id,
            )
        )
    )


def get_caretaker_with_patients_by_id(
    user_id: int, db: Session
) -> tuple[models.UserModel | None, str | None]:
    """Get a single caretaker with patients by id from the database"""
    return (
        db.query(
            models.UserModel,
            func.group_concat(
                func.distinct(models.patient_caretaker_association_table.c.patient_id)
            ).label("patient_ids"),
        )
        .outerjoin(
            models.patient_caretaker_association_table,
            models.patient_caretaker_association_table.c.caretaker_id
            == models.UserModel.id,
        )
        .options(joinedload(models.UserModel.additional_details))
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.CARETAKER,
                models.UserModel.id == user_id,
            )
        )
        .first()
    )
