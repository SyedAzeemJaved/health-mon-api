from datetime import datetime, date

from fastapi import Depends, HTTPException, APIRouter

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlite.database import get_db
from sqlalchemy.orm import Session

# Detailed
from sqlite.crud.patients.detailed import (
    # get_all_patients_with_caretakers_and_doctors_for_a_particular_user,
    get_all_patients_without_caretakers_and_doctors_for_a_particular_user,
)

# Non-detailed
from sqlite.crud.caretakers.non_detailed import (
    get_all_caretakers_by_list_of_ids,
    get_all_caretaker_ids_for_a_particular_patient,
)
from sqlite.crud.doctors.non_detailed import (
    get_all_doctors_by_list_of_ids,
    get_all_doctor_ids_for_a_particular_patient,
)

from sqlite.crud.patient_history import (
    get_last_10_patient_histories_for_particular_user,
    get_patient_histories_based_on_date_range_for_particular_user,
)

from sqlite.schemas import Patient, PatientHistory, User
from sqlite.enums import UserRoleEnum

from utils.auth import user_should_not_be_admin, get_current_user
from utils.responses import common_responses
from utils.list import return_list_of_ids

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
    if current_user.user_role == UserRoleEnum.PATIENT:
        raise HTTPException(
            status_code=403, detail="Patients can not access this route"
        )

    return paginate(
        get_all_patients_without_caretakers_and_doctors_for_a_particular_user(
            user_id=current_user.id, user_role=current_user.user_role, db=db
        ),
        transformer=lambda items: [
            Patient(
                **i.__dict__,
                caretakers=get_all_caretakers_by_list_of_ids(
                    caretaker_ids=return_list_of_ids(
                        get_all_caretaker_ids_for_a_particular_patient(
                            user_id=i.id, db=db
                        )
                    ),
                    db=db,
                ),
                doctors=get_all_doctors_by_list_of_ids(
                    doctor_ids=return_list_of_ids(
                        get_all_doctor_ids_for_a_particular_patient(user_id=i.id, db=db)
                    ),
                    db=db,
                ),
                # caretakers=get_all_caretakers_by_list_of_ids(
                #     caretaker_ids=i[1].split(",") if i[1] else [], db=db
                # ),
                # doctors=get_all_doctors_by_list_of_ids(
                #     doctor_ids=i[2].split(",") if i[2] else [], db=db
                # ),
                history=get_last_10_patient_histories_for_particular_user(
                    user_id=i.id, db=db
                )
            )
            for i in items
        ],
    )


@router.get(
    "/patients/{user_id}",
    summary="Get a single patient by id for current user's patients",
    response_model=Patient,
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

    result = get_all_patients_without_caretakers_and_doctors_for_a_particular_user(
        user_id=current_user.id, user_role=current_user.user_role, db=db
    )

    for item in result:
        if item.id == user_id:
            return Patient(
                **item.__dict__,
                caretakers=get_all_caretakers_by_list_of_ids(
                    caretaker_ids=return_list_of_ids(
                        get_all_caretaker_ids_for_a_particular_patient(
                            user_id=item.id, db=db
                        )
                    ),
                    db=db,
                ),
                doctors=get_all_doctors_by_list_of_ids(
                    doctor_ids=return_list_of_ids(
                        get_all_doctor_ids_for_a_particular_patient(
                            user_id=item.id, db=db
                        )
                    ),
                    db=db,
                ),
                history=get_last_10_patient_histories_for_particular_user(
                    user_id=item.id, db=db
                )
            )

    raise HTTPException(
        status_code=403, detail="Either patient not found or you do not have access"
    )


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

    result = get_all_patients_without_caretakers_and_doctors_for_a_particular_user(
        user_id=current_user.id, user_role=current_user.user_role, db=db
    )

    for item in result:
        if item.id == user_id:
            return paginate(
                get_patient_histories_based_on_date_range_for_particular_user(
                    user_id=user_id, start_date=start_date, end_date=end_date, db=db
                )
            )

    raise HTTPException(
        status_code=403, detail="Either patient not found or you do not have access"
    )
