import enum


class CombinedRoleEnum(str, enum.Enum):
    ADMIN = "admin"
    CARETAKER = "caretaker"
    DOCTOR = "doctor"
    PATIENT = "patient"


class UserRoleEnum(str, enum.Enum):
    CARETAKER = "caretaker"
    DOCTOR = "doctor"
    PATIENT = "patient"


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    RATHER_NOT_SAY = "rather_not_say"


class PatientBloodGroupEnum(str, enum.Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    AB_POSITIOVE = "AB+"
    AB_NEGATIVE = "AB-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "Unknown"


class PatientActionEnum(str, enum.Enum):
    ACTION_1 = "action_1"
    ACTION_2 = "action_2"
    ACTION_3 = "action_3"
    ACTION_4 = "action_4"
