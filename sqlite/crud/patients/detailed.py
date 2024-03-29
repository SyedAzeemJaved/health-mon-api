from typing import Union

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from sqlite import models

from sqlite.enums import UserRoleEnum


def get_all_patients_with_caretakers_and_doctors(
    db: Session,
) -> list[tuple[models.UserModel | None, str | None]]:
    """Get all patients with caretakers and doctors from the database"""
    return (
        db.query(
            models.UserModel,
            func.group_concat(
                func.distinct(models.patient_caretaker_association_table.c.caretaker_id)
            ).label("caretaker_ids"),
            func.group_concat(
                func.distinct(models.patient_doctor_association_table.c.doctor_id)
            ).label("doctor_ids"),
        )
        .outerjoin(
            models.patient_caretaker_association_table,
            models.patient_caretaker_association_table.c.patient_id
            == models.UserModel.id,
        )
        .outerjoin(
            models.patient_doctor_association_table,
            models.patient_doctor_association_table.c.patient_id == models.UserModel.id,
        )
        .options(
            joinedload(models.UserModel.additional_details),
        )
        .filter(models.UserModel.user_role == UserRoleEnum.PATIENT)
        .group_by(models.UserModel.id)
    )

    # # Can not use this approach
    # # As it ONLY reutrns current caretaker / doctor, instead of all that are associated with patient
    # # Because of filter on caretaker.id == user_role
    # # Which is a critical step, otherwise will return all patients
    # def get_all_patients_with_caretakers_and_doctors_for_a_particular_user(
    #     user_id: int,
    #     user_role: Union[UserRoleEnum.CARETAKER, UserRoleEnum.DOCTOR],
    #     db: Session,
    # ) -> list[tuple[models.UserModel | None, str | None, str | None]]:
    #     """Get all patients with caretakers and doctors for a particular user from the database"""
    # if user_role == UserRoleEnum.CARETAKER:
    #     return (
    #         db.query(
    #             models.UserModel,
    #             func.group_concat(
    #                 func.distinct(
    #                     models.patient_caretaker_association_table.c.caretaker_id
    #                 )
    #             ).label("caretaker_ids"),
    #             func.group_concat(
    #                 func.distinct(models.patient_doctor_association_table.c.doctor_id)
    #             ).label("doctor_ids"),
    #         )
    #         .outerjoin(
    #             models.patient_caretaker_association_table,
    #             models.patient_caretaker_association_table.c.patient_id
    #             == models.UserModel.id,
    #         )
    #         .outerjoin(
    #             models.patient_doctor_association_table,
    #             models.patient_doctor_association_table.c.patient_id
    #             == models.UserModel.id,
    #         )
    #         .options(joinedload(models.UserModel.additional_details))
    #         .filter(
    #             models.UserModel.user_role == UserRoleEnum.PATIENT,
    #             and_(
    #                 models.patient_caretaker_association_table.c.caretaker_id
    #                 == user_id,
    #                 models.patient_caretaker_association_table.c.patient_id
    #                 == models.UserModel.id,
    #             ),
    #         )
    #         .group_by(models.UserModel.id)
    #     )
    # else:
    #     return (
    #         db.query(
    #             models.UserModel,
    #             func.group_concat(
    #                 func.distinct(
    #                     models.patient_caretaker_association_table.c.caretaker_id
    #                 )
    #             ).label("caretaker_ids"),
    #             func.group_concat(
    #                 func.distinct(models.patient_doctor_association_table.c.doctor_id)
    #             ).label("doctor_ids"),
    #         )
    #         .outerjoin(
    #             models.patient_caretaker_association_table,
    #             models.patient_caretaker_association_table.c.patient_id
    #             == models.UserModel.id,
    #         )
    #         .outerjoin(
    #             models.patient_doctor_association_table,
    #             models.patient_doctor_association_table.c.patient_id
    #             == models.UserModel.id,
    #         )
    #         .options(joinedload(models.UserModel.additional_details))
    #         .filter(
    #             models.UserModel.user_role == UserRoleEnum.PATIENT,
    #             and_(
    #                 models.patient_caretaker_association_table.c.doctor_id == user_id,
    #                 models.patient_caretaker_association_table.c.patient_id
    #                 == models.UserModel.id,
    #             ),
    #         )
    #         .group_by(models.UserModel.id)
    #     )


def get_all_patients_without_caretakers_and_doctors_for_a_particular_user(
    user_id: int,
    user_role: Union[UserRoleEnum.CARETAKER, UserRoleEnum.DOCTOR],
    db: Session,
) -> list[int]:
    """Get all patients with caretakers and doctors for a particular user from the database"""
    if user_role == UserRoleEnum.CARETAKER:
        return (
            db.query(models.UserModel)
            .options(joinedload(models.UserModel.additional_details))
            .filter(
                and_(
                    models.UserModel.user_role == UserRoleEnum.PATIENT,
                    models.patient_caretaker_association_table.c.caretaker_id
                    == user_id,
                    models.patient_caretaker_association_table.c.patient_id
                    == models.UserModel.id,
                )
            )
            .group_by(models.UserModel.id)
        )
    else:
        return (
            db.query(models.UserModel)
            .options(joinedload(models.UserModel.additional_details))
            .filter(
                and_(
                    models.UserModel.user_role == UserRoleEnum.PATIENT,
                    models.patient_doctor_association_table.c.doctor_id == user_id,
                    models.patient_doctor_association_table.c.patient_id
                    == models.UserModel.id,
                )
            )
            .group_by(models.UserModel.id)
        )


def get_patient_with_caretakers_and_doctors_by_id(
    user_id: int, db: Session
) -> tuple[models.UserModel | None, str | None, str | None]:
    """Get a single patient with caretakers and doctors by id from the database"""
    return (
        db.query(
            models.UserModel,
            func.group_concat(
                func.distinct(models.patient_caretaker_association_table.c.caretaker_id)
            ).label("caretaker_ids"),
            func.group_concat(
                func.distinct(models.patient_doctor_association_table.c.doctor_id)
            ).label("doctor_ids"),
        )
        .outerjoin(
            models.patient_caretaker_association_table,
            models.patient_caretaker_association_table.c.patient_id
            == models.UserModel.id,
        )
        .outerjoin(
            models.patient_doctor_association_table,
            models.patient_doctor_association_table.c.patient_id == models.UserModel.id,
        )
        .options(joinedload(models.UserModel.additional_details))
        .filter(
            and_(
                models.UserModel.user_role == UserRoleEnum.PATIENT,
                models.UserModel.id == user_id,
            )
        )
        .first()
    )
