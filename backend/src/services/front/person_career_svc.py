from sqlalchemy.orm import Session
from daos.person_career_dao import PersonCareerDAO
from models.person import PersonModel
from schemas.person_schemas import PersonCreate

person_career_dao = PersonCareerDAO()


def create_person_career_svc(
    person: PersonModel, person_data: PersonCreate, db: Session
):
    entity_data = person_data.career.model_dump()
    entity_data["person_id"] = person.get("person_id")
    person_career_dao.create(db, entity_data)


def update_person_career_svc(person_career, person_data: PersonCreate, db: Session):
    entity_data = {
        "enrollment_year": person_data.career.enrollment_year,
        "person_career_id": person_career.get("person_career_id"),
    }
    person_career_dao.update(db, person_career.get("person_career_id"), entity_data)


def get_person_career_by_person_id_and_career_id_svc(
    person_id: int, career_id: int, db: Session
):
    return person_career_dao.get_person_career_by_person_id_and_career_id(
        person_id, career_id, db
    )
