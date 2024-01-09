from fastapi import Depends, HTTPException, APIRouter

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlite.database import get_db
from sqlalchemy.orm import Session

import sqlite.crud.patient_history as crud

from sqlite.schemas import PatientHistory, PatientHistoryCreateClass, User

from utils.auth import user_should_be_patient, get_current_user
from utils.responses import common_responses

router = APIRouter(
    prefix="/current/history",
    tags=["patient - history"],
    dependencies=[
        Depends(user_should_be_patient),
    ],
    responses=common_responses(),
)


@router.get(
    "",
    summary="Get latest patient history",
    response_model=list[PatientHistory],
)
async def get_latest_patient_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_last_10_patient_histories_for_particular_user(
        user_id=current_user.id, db=db
    )


@router.post(
    "",
    summary="Create a new patient history",
    response_model=PatientHistory,
)
async def create_patient_history(
    patient_history: PatientHistoryCreateClass,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_patient_history(
        patient_history=patient_history, db_patient=current_user, db=db
    )
