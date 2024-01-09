from sqlalchemy import and_, delete

from sqlalchemy.orm import Session
from sqlite import models


def get_caretaker_associated_with_patient(
    db_caretaker: models.UserModel, db_patient: models.UserModel, db: Session
):
    """Get caretaker associated with patient"""
    return (
        db.query(models.patient_caretaker_association_table)
        .filter(
            and_(
                models.patient_caretaker_association_table.c.caretaker_id
                == db_caretaker.id,
                models.patient_caretaker_association_table.c.patient_id
                == db_patient.id,
            )
        )
        .first()
    )


def try_associate_patient_to_caretaker(
    db_patient: models.UserModel, db_caretaker: models.UserModel, db: Session
):
    """Associate a patient to a caretaker"""
    association = models.patient_caretaker_association_table.insert().values(
        patient_id=db_patient.id, caretaker_id=db_caretaker.id
    )
    try:
        db.execute(association)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False


def try_disassociate_patient_from_caretaker(
    db_patient: models.UserModel, db_caretaker: models.UserModel, db: Session
):
    """Disassociate a patient from a caretaker"""
    try:
        db.execute(
            delete(models.patient_caretaker_association_table).where(
                (
                    models.patient_caretaker_association_table.c.patient_id
                    == db_patient.id
                )
                & (
                    models.patient_caretaker_association_table.c.caretaker_id
                    == db_caretaker.id
                )
            )
        )
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False


def get_doctor_associated_with_patient(
    db_doctor: models.UserModel, db_patient: models.UserModel, db: Session
):
    """Get doctor associated with patient"""
    return (
        db.query(models.patient_doctor_association_table)
        .filter(
            and_(
                models.patient_doctor_association_table.c.doctor_id == db_doctor.id,
                models.patient_doctor_association_table.c.patient_id == db_patient.id,
            )
        )
        .first()
    )


def try_associate_patient_to_doctor(
    db_patient: models.UserModel, db_doctor: models.UserModel, db: Session
):
    """Associate a patient to a doctor"""
    association = models.patient_doctor_association_table.insert().values(
        patient_id=db_patient.id, doctor_id=db_doctor.id
    )
    try:
        db.execute(association)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False


def try_disassociate_patient_from_doctor(
    db_patient: models.UserModel, db_doctor: models.UserModel, db: Session
):
    """Disassociate a patient from a doctor"""
    try:
        db.execute(
            delete(models.patient_doctor_association_table).where(
                (models.patient_doctor_association_table.c.patient_id == db_patient.id)
                & (models.patient_doctor_association_table.c.doctor_id == db_doctor.id)
            )
        )
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False
