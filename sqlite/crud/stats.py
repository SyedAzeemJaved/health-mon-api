from sqlalchemy.orm import Session

from sqlite import models

from sqlite.enums import CombinedRoleEnum, UserRoleEnum


def get_all_stats(db: Session):
    """Get all stats for the dashboard form the database"""
    admin_count = (
        db.query(models.UserModel)
        .filter(models.UserModel.user_role == CombinedRoleEnum.ADMIN)
        .count()
    )
    caretaker_count = (
        db.query(models.UserModel)
        .filter(models.UserModel.user_role == UserRoleEnum.CARETAKER)
        .count()
    )
    doctor_count = (
        db.query(models.UserModel)
        .filter(models.UserModel.user_role == UserRoleEnum.DOCTOR)
        .count()
    )
    patient_count = (
        db.query(models.UserModel)
        .filter(models.UserModel.user_role == UserRoleEnum.PATIENT)
        .count()
    )
    return {
        "admin_count": admin_count,
        "caretaker_count": caretaker_count,
        "doctor_count": doctor_count,
        "patient_count": patient_count,
    }
