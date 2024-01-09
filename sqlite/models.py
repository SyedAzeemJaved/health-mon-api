from datetime import datetime

from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship

from sqlite.database import Base, engine

from sqlite.schemas import UserUpdateClass
from sqlite.enums import CombinedRoleEnum, GenderEnum, PatientBloodGroupEnum

Base.metadata.create_all(bind=engine)


# ASSOCIATION TABLES
patient_caretaker_association_table = Table(
    "patient_caretaker_association_table",
    Base.metadata,
    Column(
        "patient_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "caretaker_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
)

patient_doctor_association_table = Table(
    "patient_doctor_association_table",
    Base.metadata,
    Column(
        "patient_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "doctor_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    ),
)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    user_role = Column(Enum(CombinedRoleEnum), nullable=False)

    # Define the one-to-one relationship with UserAdditionalDetailsModel
    additional_details = relationship(
        "UserAdditionalDetailsModel",
        uselist=False,
        primaryjoin="UserModel.id == UserAdditionalDetailsModel.user_id",
        cascade="all,delete",
    )

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=True, onupdate=datetime.utcnow
    )

    def update(self, user: UserUpdateClass, **kwargs):
        self.name = user.name
        self.email = user.email
        self.gender = user.gender

    def update_password(self, new_password: str, **kwargs):
        self.password = new_password


class UserAdditionalDetailsModel(Base):
    __tablename__ = "user_additional_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    phone = Column(String, unique=True, nullable=True)
    age = Column(Integer, nullable=True)
    blood_group = Column(
        Enum(PatientBloodGroupEnum),
        nullable=False,
        default=PatientBloodGroupEnum.UNKNOWN,
    )

    def update(self, user: UserUpdateClass, **kwargs):
        self.phone = user.additional_details.phone
        self.age = user.additional_details.age
        self.blood_group = user.additional_details.blood_group


class PatientHistoryModel(Base):
    __tablename__ = "patient_histories"

    id = Column(Integer, primary_key=True)

    patient_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )

    spo2_reading = Column(Float, nullable=False, default=0.0)
    bp_reading = Column(Float, nullable=False, default=0.0)
    temp_reading = Column(Float, nullable=False, default=0.0)
    heartbeat_reading = Column(Float, nullable=False, default=0.0)

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
