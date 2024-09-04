from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.front.person_subject_svc import (
    create_person_subject_svc,
    get_person_subject_by_person_id_and_subject_id_svc,
    update_person_subject_svc,
)
from services.front.person_career_svc import (
    create_person_career_svc,
    get_person_career_by_person_id_and_career_id_svc,
    update_person_career_svc,
)
from models.career import CareerModel
from services.front.career_svc import get_career_by_id_svc
from models.person import PersonModel
from schemas.person_schemas import PersonCreate, PersonCreateResponse, PersonResponse
from services.front.person_svc import (
    create_person_svc,
    get_person_by_email_svc,
    get_all_persons_svc,
    get_person_by_id_svc,
)
from utils.functions import filter_fields
from database import get_db
from pydantic import EmailStr


person_router = APIRouter(
    prefix="/person",
    tags=["Person"],
)


@person_router.get("/check_email_exists")
async def check_email_exists_route(email: EmailStr, db: Session = Depends(get_db)):
    return get_person_by_email_svc(email, db) is not None


@person_router.get("/get/{person_id}")
async def get_person_route(person_id: int, db: Session = Depends(get_db)):
    person = get_person_by_id_svc(person_id, db)
    if person:
        return PersonResponse(**dict(person))
    else:
        return {"message": "Person not found"}


@person_router.get("/get_all")
async def get_all_persons_route(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    if skip < 0 or limit < 0:
        raise HTTPException(
            status_code=400, detail="Skip and limit must be greater than 0"
        )
    response = [
        PersonResponse(**dict(person))
        for person in get_all_persons_svc(skip, limit, db)
    ]
    return {"persons": response, "total_rows": len(response)}


@person_router.post("/register")
async def register_person_route(
    person_data: PersonCreate, db: Session = Depends(get_db)
):
    career_db: CareerModel = get_career_by_id_svc(person_data, db)
    if not career_db:
        raise HTTPException(
            status_code=400,
            detail="Career not found or subject does not belong to career",
        )

    person: PersonModel = get_person_by_email_svc(person_data.person_email, db)

    if not person:
        person: PersonModel = create_person_svc(
            filter_fields(person_data, PersonModel), db
        )
        person = person.__dict__
        create_person_career_svc(person, person_data, db)
        create_person_subject_svc(person, person_data, db)
    else:
        person_career = get_person_career_by_person_id_and_career_id_svc(
            person.get("person_id"), person_data.career.career_id, db
        )
        person_subject = get_person_subject_by_person_id_and_subject_id_svc(
            person.get("person_id"), person_data.subject.subject_id, db
        )
        if not person_career:
            create_person_career_svc(person, person_data, db)
        else:
            update_person_career_svc(person_career, person_data, db)
        if not person_subject:
            create_person_subject_svc(person, person_data, db)
        else:
            update_person_subject_svc(person_subject, person_data, db)

    return {
        "message": "Person created successfully",
        "person": PersonCreateResponse(**dict(person)),
    }
