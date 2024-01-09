from fastapi import Depends, HTTPException, APIRouter

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlite.database import get_db
from sqlalchemy.orm import Session

from sqlite.crud.caretakers.detailed import (
    get_all_caretakers_with_patients,
    get_caretaker_with_patients_by_id,
)
from sqlite.crud.patients.non_detailed import get_all_patients_by_list_of_ids

from sqlite.schemas import CaretakerOrDoctor

from utils.auth import user_should_be_admin
from utils.responses import common_responses

router = APIRouter(
    prefix="/caretakers",
    tags=["admin - caretakers"],
    dependencies=[
        Depends(user_should_be_admin),
    ],
    responses=common_responses(),
)


@router.get(
    "",
    summary="Get a list of all caretakers (detailed)",
    response_model=Page[CaretakerOrDoctor],
)
async def get_all_detailed_caretakers(db: Session = Depends(get_db)):
    return paginate(
        get_all_caretakers_with_patients(db=db),
        transformer=lambda items: [
            CaretakerOrDoctor(
                **i[0].__dict__,
                patients=get_all_patients_by_list_of_ids(
                    patient_ids=i[1].split(",") if i[1] else [], db=db
                )
            )
            for i in items
            if i[0]
        ],
    )


@router.get(
    "/{user_id}",
    summary="Get a single caretaker (detailed) by id",
    response_model=CaretakerOrDoctor,
)
async def get_detailed_caretaker_by_id(user_id: int, db: Session = Depends(get_db)):
    result = get_caretaker_with_patients_by_id(user_id=user_id, db=db)
    if result[0] is None:
        raise HTTPException(status_code=404, detail="Caretaker not found")
    return CaretakerOrDoctor(
        **result[0].__dict__,
        patients=get_all_patients_by_list_of_ids(
            patient_ids=result[1].split(",") if result[1] else [], db=db
        )
    )
