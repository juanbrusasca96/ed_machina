from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.front.career_subject_svc import CareerSubjectService
from models.subject import SubjectModel
from services.front.subject_svc import SubjectService
from services.front.person_subject_svc import (
    PersonSubjectService,
)
from services.front.person_career_svc import (
    PersonCareerService,
)
from models.career import CareerModel
from services.front.career_svc import CareerService
from models.person import PersonModel
from schemas.person_schemas import PersonCreate, PersonCreateResponse, PersonResponse
from services.front.person_svc import (
    PersonService,
)
from utils.functions import filter_fields, get_dict_from_list, to_dict
from database import get_db
from pydantic import EmailStr


person_router = APIRouter(
    prefix="/person",
    tags=["Person"],
)


@person_router.get("/check_email_exists")
async def check_email_exists_route(email: EmailStr, db: Session = Depends(get_db)):
    person_service = PersonService(db)

    return (
        person_service.get_by_field(
            PersonModel.person_email.name, email.strip().lower()
        )
        is not None
    )


@person_router.get("/get/{person_id}")
async def get_person_route(person_id: int, db: Session = Depends(get_db)):
    person_service = PersonService(db)
    career_service = CareerService(db)
    subject_service = SubjectService(db)

    person = person_service.get_by_id(person_id)
    if person:
        person = to_dict(person)
        person_id = person.get("person_id")
        careers = career_service.get_related_careers((person_id,))
        subjects = subject_service.get_related_subjects((person_id,))
        person["careers"] = careers
        person["subjects"] = subjects
        return PersonResponse(**dict(person))
    else:
        return {"message": "Person not found"}


@person_router.get("/get_all")
async def get_all_persons_route(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    person_service = PersonService(db)
    career_service = CareerService(db)
    subject_service = SubjectService(db)

    if skip < 0 or limit < 0:
        raise HTTPException(
            status_code=400, detail="Skip and limit must be greater than 0"
        )

    response = []
    persons: list[PersonModel] = person_service.get_all(skip, limit)
    if persons:
        person_ids = tuple(person.person_id for person in persons)
        careers = get_dict_from_list(
            career_service.get_related_careers(person_ids), "person_id"
        )
        subjects = get_dict_from_list(
            subject_service.get_related_subjects(person_ids), "person_id"
        )

        for person in persons:
            person = to_dict(person)
            person_id = person.get("person_id")
            person["careers"] = careers.get(person_id, [])
            person["subjects"] = subjects.get(person_id, [])
            response.append(PersonResponse(**dict(person)))

    return {"persons": response, "total_rows": person_service.count()}


@person_router.post("/register")
async def register_person_route(
    person_data: PersonCreate, db: Session = Depends(get_db)
):
    career_service = CareerService(db)
    person_service = PersonService(db)
    person_career_service = PersonCareerService(db)
    person_subject_service = PersonSubjectService(db)
    career_subject_service = CareerSubjectService(db)

    career_db: CareerModel = career_service.get_by_id(person_data.career.career_id)
    if not career_db:
        raise HTTPException(
            status_code=400,
            detail="Career not found",
        )

    career_subject_db = career_subject_service.get_by_fields(
        {
            CareerModel.career_id.name: career_db.career_id,
            SubjectModel.subject_id.name: person_data.subject.subject_id,
        }
    )
    if not career_subject_db:
        raise HTTPException(
            status_code=400,
            detail="Subject not found in career",
        )

    person: PersonModel = person_service.get_by_field(
        PersonModel.person_email.name, person_data.person_email
    )

    if not person:
        person: PersonModel = person_service.create(
            filter_fields(person_data, PersonModel)
        )
        person_career_service.create(
            {
                PersonModel.person_id.name: person.person_id,
                **person_data.career.model_dump(),
            }
        )
        person_subject_service.create(
            {
                PersonModel.person_id.name: person.person_id,
                **person_data.subject.model_dump(),
            }
        )
    else:
        person_career = person_career_service.get_by_fields(
            {
                PersonModel.person_id.name: person.person_id,
                CareerModel.career_id.name: person_data.career.career_id,
            }
        )
        person_subject = person_subject_service.get_by_fields(
            {
                PersonModel.person_id.name: person.person_id,
                SubjectModel.subject_id.name: person_data.subject.subject_id,
            }
        )
        if not person_career:
            person_career_service.create(
                {
                    PersonModel.person_id.name: person.person_id,
                    **person_data.career.model_dump(),
                }
            )
        else:
            person_career_service.update(
                person_career.person_career_id,
                {
                    "enrollment_year": person_data.career.enrollment_year,
                },
            )
        if not person_subject:
            person_subject_service.create(
                {
                    PersonModel.person_id.name: person.person_id,
                    **person_data.subject.model_dump(),
                }
            )
        else:
            person_subject_service.update(
                person_subject.person_subject_id,
                {
                    "study_time": person_subject.study_time
                    + person_data.subject.study_time,
                    "subject_attempts": person_subject.subject_attempts
                    + person_data.subject.subject_attempts,
                },
            )

    return {
        "message": "Person created successfully",
        "person": PersonCreateResponse(**to_dict(person)),
    }
