from datetime import datetime, date, timedelta
from pydantic import BaseModel, ConfigDict, field_validator

from sqlite.enums import (
    CombinedRoleEnum,
    UserRoleEnum,
    PatientBloodGroupEnum,
    GenderEnum,
    PatientActionEnum,
)

from utils.date_utils import (
    convert_datetime_to_iso_8601_with_z_suffix,
    get_current_datetime_in_str_iso_8601_with_z_suffix,
)


def replace_empty_strings_with_null(cls, value):
    """Replace empty strings, or 'string' to None/null"""
    if isinstance(value, str):
        if value == "string" or value.strip() == "":
            return None
    return value


class Token(BaseModel):
    access_token: str
    token_type: str
    user: "User"


class TokenData(BaseModel):
    email: str | None = None


class CommonResponseClass(BaseModel):
    detail: str


# UserAdditionalDetails
class UserAdditionalDetailsBaseClass(BaseModel):
    phone: str | None = None
    age: int | None = None
    blood_group: PatientBloodGroupEnum = PatientBloodGroupEnum.UNKNOWN

    @field_validator("*", mode="after")
    @classmethod
    def replace_empty_strings_with_null(cls, value):
        return replace_empty_strings_with_null(cls=cls, value=value)

    @field_validator("age")
    @classmethod
    def age_validator(cls, value: int | None):
        if isinstance(value, int):
            if not (value > 0 and value < 150):
                raise ValueError("age must be a positive and less than 150")
            return value
        return None


class UserAdditionalDetailsCreateOrUpdateClass(UserAdditionalDetailsBaseClass):
    pass


class UserAdditionalDetails(UserAdditionalDetailsBaseClass):
    model_config = ConfigDict(from_attributes=True)


# User
class UserBaseClass(BaseModel):
    name: str
    email: str
    gender: GenderEnum

    @field_validator("email")
    @classmethod
    def email_validator(cls, v: str) -> str:
        if " " in v:
            raise ValueError("must not contain a space")
        if "," in v:
            raise ValueError("must not contain any commas")
        if not "@" in v:
            raise ValueError("must be a valid email address")
        return v


class UserCreateClass(UserBaseClass):
    password: str
    user_role: CombinedRoleEnum


class UserUpdateClass(UserBaseClass):
    additional_details: UserAdditionalDetailsCreateOrUpdateClass


class UserPasswordUpdateClass(BaseModel):
    new_password: str


# User
## Note: Can or can not be an admin
class User(UserBaseClass):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: convert_datetime_to_iso_8601_with_z_suffix,
        },
    )

    id: int

    additional_details: UserAdditionalDetails
    user_role: CombinedRoleEnum

    created_at: datetime = get_current_datetime_in_str_iso_8601_with_z_suffix()
    updated_at: datetime | None = get_current_datetime_in_str_iso_8601_with_z_suffix()


## Note: Can not be an admin - can be UserRoleEnum.CARETAKER, UserRoleEnum.DOCTOR or UserRoleEnum.PATIENT
class UserWhoIsNotAnAdminBaseClass(User):
    user_role: UserRoleEnum


# Caretaker or Doctor
class CaretakerOrDoctor(UserWhoIsNotAnAdminBaseClass):
    patients: list[UserWhoIsNotAnAdminBaseClass]


# Patient
class Patient(UserWhoIsNotAnAdminBaseClass):
    caretakers: list[UserWhoIsNotAnAdminBaseClass]
    doctors: list[UserWhoIsNotAnAdminBaseClass]
    history: list["PatientHistory"]


# Patient History
class PatientHistoryBaseClass(BaseModel):
    spo2_reading: float
    systolic_reading: int
    diastolic_reading: int
    temp_reading: float
    heartbeat_reading: float

    @field_validator("*")
    @classmethod
    def value_validator(cls, v: float | int) -> float | int:
        if isinstance(v, float | int):
            if v <= 0:
                raise ValueError("must be a positive value")
        return v


class PatientHistoryCreateClass(PatientHistoryBaseClass):
    pass


class PatientHistory(PatientHistoryBaseClass):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: convert_datetime_to_iso_8601_with_z_suffix,
        },
    )

    id: int

    created_at: datetime


# Patient Action
class PatientActionBaseClass(BaseModel):
    action: PatientActionEnum


# Stats
class StatsBaseClass(BaseModel):
    admin_count: int
    caretaker_count: int
    doctor_count: int
    patient_count: int


Token.model_rebuild()
Patient.model_rebuild()
