from fastapi import Depends, HTTPException, APIRouter

from sqlite.database import get_db
from sqlalchemy.orm import Session

# import sqlite.crud.patient_history as crud

from sqlite.schemas import PatientAction, User

from utils.auth import user_should_be_patient, get_current_user
from utils.responses import common_responses

router = APIRouter(
    prefix="/current/actions",
    tags=["patient - actions"],
    dependencies=[
        Depends(user_should_be_patient),
    ],
    responses=common_responses(),
)


@router.post(
    "",
    summary="Send patient action notification to all caretakers for current patient",
    response_model=PatientAction,
)
async def call_patient_action(
    patient_action: PatientAction,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # return crud.create_patient_history(
    #     patient_history=patient_history, db_patient=current_user, db=db
    # )
    return patient_action
