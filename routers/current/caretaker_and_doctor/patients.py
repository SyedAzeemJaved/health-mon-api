from datetime import datetime, date

from fastapi import Depends, HTTPException, APIRouter

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlite.database import get_db
from sqlalchemy.orm import Session

# Detailed
from sqlite.crud.patients.detailed import (
    get_all_patients_with_caretakers_and_doctors_for_a_particular_user,
    get_all_patients_with_caretakers_and_doctors,
)

# Non-detailed
from sqlite.crud.caretakers.non_detailed import get_all_caretakers_by_list_of_ids
from sqlite.crud.doctors.non_detailed import get_all_doctors_by_list_of_ids

from sqlite.crud.patient_history import (
    get_last_10_patient_histories_for_particular_user,
    get_patient_histories_based_on_date_range_for_particular_user,
)

from sqlite.schemas import Patient, PatientHistory, User
from sqlite.enums import UserRoleEnum

from utils.auth import user_should_not_be_admin, get_current_user
from utils.responses import common_responses

router = APIRouter(
    prefix="/current",
    tags=["caretaker and doctor - patients"],
    dependencies=[
        Depends(user_should_not_be_admin),
    ],
    responses=common_responses(),
)


async def validate_date_range(start_date: date, end_date: date):
    # Check if start_date is less than end_date
    if start_date >= end_date:
        raise HTTPException(
            status_code=403, detail="Start date should be less than end date"
        )
    # Check if end_date is not greater than today date
    if end_date > datetime.utcnow().date():
        raise HTTPException(
            status_code=403, detail="End time should not be greater than today"
        )


@router.get(
    "/patients",
    summary="Get a list of patients for current user's patients",
    response_model=Page[Patient],
)
async def get_everyone_for_patients_of_current_user(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    # remove import from top
    return paginate(
        get_all_patients_with_caretakers_and_doctors(db=db),
        transformer=lambda items: [
            Patient(
                **i[0].__dict__,
                caretakers=get_all_caretakers_by_list_of_ids(
                    caretaker_ids=i[1].split(",") if i[1] else [], db=db
                ),
                doctors=get_all_doctors_by_list_of_ids(
                    doctor_ids=i[2].split(",") if i[2] else [], db=db
                ),
                history=get_last_10_patient_histories_for_particular_user(
                    user_id=4, db=db
                )
            )
            for i in items
            if i[0]
        ],
    )

    if current_user.user_role == UserRoleEnum.CARETAKER:
        return paginate(
            get_all_patients_with_caretakers_and_doctors_for_a_particular_user(
                user_id=current_user.id, db=db
            ),
            transformer=lambda items: [
                Patient(
                    **i[0].__dict__,
                    caretakers=get_all_caretakers_by_list_of_ids(
                        caretaker_ids=i[1].split(",") if i[1] else [], db=db
                    ),
                    doctors=get_all_doctors_by_list_of_ids(
                        doctor_ids=i[2].split(",") if i[2] else [], db=db
                    ),
                    history=get_last_10_patient_histories_for_particular_user(
                        user_id=current_user.id, db=db
                    )
                )
                for i in items
                if i[0]
            ],
        )
    elif current_user.user_role == UserRoleEnum.DOCTOR:
        return paginate(
            get_all_patients_with_caretakers_and_doctors_for_a_particular_user(
                user_id=current_user.id, db=db
            ),
            transformer=lambda items: [
                Patient(
                    **i[0].__dict__,
                    caretakers=get_all_caretakers_by_list_of_ids(
                        caretaker_ids=i[1].split(",") if i[1] else [], db=db
                    ),
                    doctors=get_all_doctors_by_list_of_ids(
                        doctor_ids=i[2].split(",") if i[2] else [], db=db
                    ),
                    history=get_last_10_patient_histories_for_particular_user(
                        user_id=current_user.id, db=db
                    )
                )
                for i in items
                if i[0]
            ],
        )
    else:
        raise HTTPException(
            status_code=403, detail="Patients can not access this route"
        )


@router.get(
    "/patients/{user_id}",
    summary="Get a single patient by id for current user's patients",
    # response_model=Patient,
)
async def get_patient_by_id_for_patients_of_current_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.user_role == UserRoleEnum.PATIENT:
        raise HTTPException(
            status_code=403, detail="Patients can not access this route"
        )

    # result = get_all_patients_with_caretakers_and_doctors_for_a_particular_user(
    #     user_id=current_user.id, db=db
    # )

    # for item in result:
    #     if item[0]:
    #         if item[0].id == user_id:
    #             return Patient(
    #                 **item[0].__dict__,
    #                 caretakers=get_all_caretakers_by_list_of_ids(
    #                     caretaker_ids=item[1].split(",") if item[1] else [], db=db
    #                 ),
    #                 doctors=get_all_doctors_by_list_of_ids(
    #                     doctor_ids=item[2].split(",") if item[2] else [], db=db
    #                 ),
    #                 history=get_last_10_patient_histories_for_particular_user(
    #                     user_id=current_user.id, db=db
    #                 )
    #             )

    # raise HTTPException(
    #     status_code=403, detail="Either patient not found or you do not have access"
    # )

    return {
        "name": "Ani Daah",
        "email": "ani_daah@email.com",
        "gender": "female",
        "id": 4,
        "additional_details": {
            "phone": None,
            "age": 22,
            "blood_group": "Unknown",
        },
        "user_role": "patient",
        "created_at": "2024-01-04T00:56:26Z",
        "updated_at": None,
        "caretakers": [
            {
                "name": "Caretaker",
                "email": "c@email.com",
                "gender": "male",
                "id": 2,
                "additional_details": {
                    "phone": None,
                    "age": None,
                    "blood_group": "Unknown",
                },
                "user_role": "caretaker",
                "created_at": "2024-01-04T00:54:58Z",
                "updated_at": None,
            }
        ],
        "doctors": [
            {
                "name": "Doctor",
                "email": "d@email.com",
                "gender": "male",
                "id": 3,
                "additional_details": {
                    "phone": None,
                    "age": None,
                    "blood_group": "Unknown",
                },
                "user_role": "doctor",
                "created_at": "2024-01-04T00:55:57Z",
                "updated_at": None,
            }
        ],
        "history": [
            {
                "spo2_reading": 12,
                "bp_reading": 23,
                "temp_reading": 34,
                "heartbeat_reading": 45,
                "id": 3,
                "created_at": "2024-01-06T22:10:43Z",
            },
            {
                "spo2_reading": 11,
                "bp_reading": 22,
                "temp_reading": 33,
                "heartbeat_reading": 44,
                "id": 2,
                "created_at": "2024-01-06T22:10:27Z",
            },
            {
                "spo2_reading": 10,
                "bp_reading": 20,
                "temp_reading": 30,
                "heartbeat_reading": 40,
                "id": 1,
                "created_at": "2024-01-06T22:10:12Z",
            },
            {
                "spo2_reading": 12,
                "bp_reading": 23,
                "temp_reading": 34,
                "heartbeat_reading": 45,
                "id": 3,
                "created_at": "2024-01-06T22:10:43Z",
            },
            {
                "spo2_reading": 11,
                "bp_reading": 22,
                "temp_reading": 33,
                "heartbeat_reading": 44,
                "id": 2,
                "created_at": "2024-01-06T22:10:27Z",
            },
            {
                "spo2_reading": 10,
                "bp_reading": 20,
                "temp_reading": 30,
                "heartbeat_reading": 40,
                "id": 1,
                "created_at": "2024-01-06T22:10:12Z",
            },
            {
                "spo2_reading": 12,
                "bp_reading": 23,
                "temp_reading": 34,
                "heartbeat_reading": 45,
                "id": 3,
                "created_at": "2024-01-06T22:10:43Z",
            },
            {
                "spo2_reading": 11,
                "bp_reading": 22,
                "temp_reading": 33,
                "heartbeat_reading": 44,
                "id": 2,
                "created_at": "2024-01-06T22:10:27Z",
            },
            {
                "spo2_reading": 10,
                "bp_reading": 20,
                "temp_reading": 30,
                "heartbeat_reading": 40,
                "id": 1,
                "created_at": "2024-01-06T22:10:12Z",
            },
            {
                "spo2_reading": 12,
                "bp_reading": 23,
                "temp_reading": 34,
                "heartbeat_reading": 45,
                "id": 3,
                "created_at": "2024-01-06T22:10:43Z",
            },
        ],
    }


@router.get(
    "/patients/history/{user_id}/{start_date}/{end_date}",
    summary="Get a patient history for a date range by id for current user's patients",
    response_model=Page[PatientHistory],
)
async def get_patient_history_for_date_range_by_id_for_patients_of_current_user(
    user_id: int,
    start_date: date,
    end_date: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.user_role == UserRoleEnum.PATIENT:
        raise HTTPException(
            status_code=403, detail="Patients can not access this route"
        )

    # Validate date range
    await validate_date_range(start_date=start_date, end_date=end_date)

    result = get_all_patients_with_caretakers_and_doctors_for_a_particular_user(
        user_id=current_user.id, db=db
    )

    for item in result:
        if item[0]:
            if item[0].id == user_id:
                return paginate(
                    get_patient_histories_based_on_date_range_for_particular_user(
                        user_id=user_id, start_date=start_date, end_date=end_date, db=db
                    )
                )

    raise HTTPException(
        status_code=403, detail="Either patient not found or you do not have access"
    )
