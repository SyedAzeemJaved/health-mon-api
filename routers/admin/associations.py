from fastapi import Depends, HTTPException, APIRouter

from sqlite.database import get_db
from sqlalchemy.orm import Session

import sqlite.crud.associations as associations
from sqlite.crud.caretakers.non_detailed import get_caretaker_by_id
from sqlite.crud.doctors.non_detailed import get_doctor_by_id
from sqlite.crud.patients.non_detailed import get_patient_by_id

from sqlite.schemas import CommonResponseClass

from utils.auth import user_should_be_admin
from utils.responses import common_responses


router = APIRouter(
    prefix="/associations",
    tags=["admin - associations"],
    dependencies=[
        Depends(user_should_be_admin),
    ],
    responses=common_responses(),
)


@router.post(
    "/caretaker",
    summary="Associate a patient with a caretaker",
    response_model=CommonResponseClass,
)
async def associate_caretaker(
    patient_id: int, caretaker_id: int, db: Session = Depends(get_db)
):
    db_patient = get_patient_by_id(user_id=patient_id, db=db)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_caretaker = get_caretaker_by_id(user_id=caretaker_id, db=db)
    if db_caretaker is None:
        raise HTTPException(status_code=404, detail="Caretaker not found")
    if associations.get_caretaker_associated_with_patient(
        db_caretaker=db_caretaker, db_patient=db_patient, db=db
    ):
        raise HTTPException(
            status_code=403, detail="Caretaker is already associated with this patient"
        )
    did_patient_associate = associations.try_associate_patient_to_caretaker(
        db_patient=db_patient, db_caretaker=db_caretaker, db=db
    )
    if did_patient_associate:
        return {"detail": "Associated successfully"}
    else:
        return {"detail": "Failed to associate"}


@router.post(
    "/disassociate/caretaker",
    summary="Disassociate a patient from a caretaker",
    response_model=CommonResponseClass,
)
def disassociate_caretaker(
    patient_id: int, caretaker_id: int, db: Session = Depends(get_db)
):
    db_patient = get_patient_by_id(user_id=patient_id, db=db)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_caretaker = get_caretaker_by_id(user_id=caretaker_id, db=db)
    if db_caretaker is None:
        raise HTTPException(status_code=404, detail="Caretaker not found")
    did_patient_disassociate = associations.try_disassociate_patient_from_caretaker(
        db_patient=db_patient, db_caretaker=db_caretaker, db=db
    )
    if did_patient_disassociate:
        return {"detail": "Disassociated successfully"}
    else:
        return {"detail": "Failed to disassocaite"}


@router.post(
    "/doctor",
    summary="Associate a patient with a doctor",
    response_model=CommonResponseClass,
)
async def associate_doctor(
    patient_id: int, doctor_id: int, db: Session = Depends(get_db)
):
    db_patient = get_patient_by_id(user_id=patient_id, db=db)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_doctor = get_doctor_by_id(user_id=doctor_id, db=db)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if associations.get_doctor_associated_with_patient(
        db_doctor=db_doctor, db_patient=db_patient, db=db
    ):
        raise HTTPException(
            status_code=403, detail="Doctor is already associated with this patient"
        )
    did_patient_associate = associations.try_associate_patient_to_doctor(
        db_patient=db_patient, db_doctor=db_doctor, db=db
    )
    if did_patient_associate:
        return {"detail": "Associated successfully"}
    else:
        return {"detail": "Failed to associate"}


@router.post(
    "/disassociate/doctor",
    summary="Disassociate a patient from a doctor",
    response_model=CommonResponseClass,
)
def disassociate_doctor(patient_id: int, doctor_id: int, db: Session = Depends(get_db)):
    db_patient = get_patient_by_id(user_id=patient_id, db=db)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_doctor = get_doctor_by_id(user_id=doctor_id, db=db)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    did_patient_disassociate = associations.try_disassociate_patient_from_doctor(
        db_patient=db_patient, db_doctor=db_doctor, db=db
    )
    if did_patient_disassociate:
        return {"detail": "Disassociated successfully"}
    else:
        return {"detail": "Failed to disassocaite"}
