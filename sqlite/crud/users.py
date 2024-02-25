from datetime import datetime

from sqlalchemy.orm import Session, joinedload, selectinload

from sqlite import models

from sqlite.schemas import (
    UserCreateClass,
    UserUpdateClass,
    UserPasswordUpdateClass,
)

from utils.password import get_password_hash


def get_all_users(db: Session):
    """Get all users from the database"""
    return db.query(models.UserModel).options(
        joinedload(models.UserModel.additional_details)
    )


def get_user_by_id(user_id: int, db: Session):
    """Get a single user by id from the database"""
    return (
        db.query(models.UserModel)
        .options(joinedload(models.UserModel.additional_details))
        .filter(models.UserModel.id == user_id)
        .first()
    )


def get_user_by_email(user_email: str, db: Session):
    """Get a single user by email from the database"""
    return (
        db.query(models.UserModel)
        .options(joinedload(models.UserModel.additional_details))
        .filter(models.UserModel.email == user_email)
        .first()
    )


def get_user_by_phone(user_phone: str, db: Session):
    """Get a single user by phone from the database"""
    return (
        db.query(models.UserModel)
        .join(models.UserModel.additional_details)
        .options(joinedload(models.UserModel.additional_details))
        .filter(models.UserAdditionalDetailsModel.phone == user_phone)
        .first()
    )


def get_detailed_user(db_user: models.UserModel, db: Session):
    """Get a detailed single user from the database"""
    return (
        db.query(
            models.UserModel, models.patient_caretaker_association_table.c.caretaker_id
        )
        .outerjoin(
            models.patient_caretaker_association_table,
            models.patient_caretaker_association_table.c.patient_id
            == models.UserModel.id,
        )
        .options(selectinload(models.UserModel.additional_details))
        .filter(models.UserModel.id == db_user.id)
        .first()
    )


def create_user_with_additional_details(user: UserCreateClass, db: Session):
    """Create a new user, along with it's additional details in the database"""
    user.password = get_password_hash(user.password)
    db_user = models.UserModel(**user.__dict__)
    db_user.additional_details = models.UserAdditionalDetailsModel()
    db.add(db_user)
    db.commit()

    return db_user


def update_user(user: UserUpdateClass, db_user: models.UserModel, db: Session):
    """Update a user, along with it's additional details in the database"""
    db_user.update(user)
    db_user.additional_details.update(user)
    # Need to manually update updated_at
    # Else if only UserAdditionalDetailsModel model is updated, updated_at will not trigger
    db_user.updated_at = datetime.utcnow()
    db.commit()

    return db_user


def update_user_password(
    new_password: UserPasswordUpdateClass, db_user: models.UserModel, db: Session
):
    """Update a user's password on the database"""
    new_password.new_password = get_password_hash(password=new_password.new_password)
    db_user.update_password(new_password=new_password.new_password)
    db.commit()

    return db_user


def delete_user(db_user: models.UserModel, db: Session):
    """Delete a user from the database"""
    # Cascade will handle delete from PatientModel, CaretakerModel or DoctorModel
    db.delete(db_user)
    # UserAssociationDetails is on cascade, it will be deleted automatically
    db.commit()

    return {"detail": "Deleted successfully"}
