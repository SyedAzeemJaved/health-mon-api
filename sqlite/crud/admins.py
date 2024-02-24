from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from sqlite import models
from sqlite.enums import CombinedRoleEnum


def get_all_admins(db: Session):
    """Get all admins from the database"""
    return (
        db.query(models.UserModel)
        .options(joinedload(models.UserModel.additional_details))
        .filter(models.UserModel.user_role == CombinedRoleEnum.ADMIN)
    )


def get_admin_by_id(user_id: int, db: Session):
    """Get a single admin by id from the database"""
    return (
        db.query(models.UserModel)
        .options(joinedload(models.UserModel.additional_details))
        .filter(
            and_(
                models.UserModel.user_role == CombinedRoleEnum.ADMIN,
                models.UserModel.id == user_id,
            )
        )
        .first()
    )
