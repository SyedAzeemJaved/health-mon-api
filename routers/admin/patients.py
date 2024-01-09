from fastapi import Depends, HTTPException, APIRouter

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlite.database import get_db
from sqlalchemy.orm import Session

from sqlite.crud.patients.detailed import (
    get_all_patients_with_caretakers_and_doctors,
    get_patient_with_caretakers_and_doctors_by_id,
)
from sqlite.crud.caretakers.non_detailed import get_all_caretakers_by_list_of_ids
from sqlite.crud.doctors.non_detailed import get_all_doctors_by_list_of_ids

from sqlite.crud.patient_history import (
    get_last_10_patient_histories_for_particular_user,
)

from sqlite.schemas import Patient

from utils.auth import user_should_be_admin
from utils.responses import common_responses

router = APIRouter(
    prefix="/patients",
    tags=["admin - patients"],
    dependencies=[
        Depends(user_should_be_admin),
    ],
    responses=common_responses(),
)


@router.get(
    "",
    summary="Get a list of all patients (detailed)",
    response_model=Page[Patient],
)
async def get_all_detailed_patients(db: Session = Depends(get_db)):
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
                    user_id=i[0].id, db=db
                )
            )
            for i in items
            if i[0]
        ],
    )


@router.get(
    "/{user_id}",
    summary="Get a single patient (detailed) by id",
    response_model=Patient,
)
async def get_detailed_patient_by_id(user_id: int, db: Session = Depends(get_db)):
    result = get_patient_with_caretakers_and_doctors_by_id(user_id=user_id, db=db)
    if result[0] is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return Patient(
        **result[0].__dict__,
        caretakers=get_all_caretakers_by_list_of_ids(
            caretaker_ids=result[1].split(",") if result[1] else [], db=db
        ),
        doctors=get_all_doctors_by_list_of_ids(
            doctor_ids=result[2].split(",") if result[2] else [], db=db
        ),
        history=get_last_10_patient_histories_for_particular_user(
            user_id=result[0].id, db=db
        )
    )
