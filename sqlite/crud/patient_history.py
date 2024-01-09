from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from sqlite import models

from sqlite.schemas import PatientHistoryCreateClass, User


def get_last_10_patient_histories_for_particular_user(user_id: int, db: Session):
    """Get last 10 patient histories for a particular user from the database"""
    return (
        db.query(models.PatientHistoryModel)
        .filter(models.PatientHistoryModel.patient_id == user_id)
        .order_by(desc(models.PatientHistoryModel.created_at))
        .limit(10)
        .all()
    )


def get_patient_histories_based_on_date_range_for_particular_user(
    user_id: int, start_date: date, end_date: date, db: Session
):
    """Get all patient histories for a particular user based on provided date range from the database"""
    return (
        db.query(models.PatientHistoryModel)
        .filter(
            and_(
                models.PatientHistoryModel.patient_id == user_id,
                models.PatientHistoryModel.created_at >= start_date,
                models.PatientHistoryModel.created_at <= end_date,
            )
        )
        .order_by(desc(models.PatientHistoryModel.created_at))
    )


def create_patient_history(
    patient_history: PatientHistoryCreateClass, db_patient: User, db: Session
):
    """Create a new patient history in the database"""
    db_patient_history = models.PatientHistoryModel(
        **patient_history.__dict__, patient_id=db_patient.id
    )
    db.add(db_patient_history)
    db.commit()

    return db_patient_history
