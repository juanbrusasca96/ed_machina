from daos.person_subject_dao import PersonSubjectDAO
from models.person import PersonModel
from schemas.person_schemas import PersonCreate
from sqlalchemy.orm import Session

person_subject_dao = PersonSubjectDAO()


def create_person_subject_svc(
    person: PersonModel, person_data: PersonCreate, db: Session
):
    entity_data = person_data.subject.model_dump()
    entity_data["person_id"] = person.get("person_id")
    person_subject_dao.create(db, entity_data)


def update_person_subject_svc(person_subject, person_data: PersonCreate, db: Session):
    entity_data = {
        "study_time": person_subject.get("study_time") + person_data.subject.study_time,
        "subject_attempts": person_subject.get("subject_attempts")
        + person_data.subject.subject_attempts,
        "person_subject_id": person_subject.get("person_subject_id"),
    }
    person_subject_dao.update(db, person_subject.get("person_subject_id"), entity_data)


def get_person_subject_by_person_id_and_subject_id_svc(
    person_id: int, subject_id: int, db: Session
):
    return person_subject_dao.get_person_subject_by_person_id_and_subject_id(
        person_id, subject_id, db
    )
