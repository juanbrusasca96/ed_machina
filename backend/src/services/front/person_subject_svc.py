from daos.person_subject_dao import PersonSubjectDAO
from models.person import PersonModel
from schemas.person_schemas import PersonCreate
from sqlalchemy.orm import Session


def create_person_subject_svc(
    person: PersonModel, person_data: PersonCreate, db: Session
):
    PersonSubjectDAO.create_person_subject(person, person_data, db)


def update_person_subject_svc(person_subject, person_data: PersonCreate, db: Session):
    PersonSubjectDAO.update_person_subject(person_subject, person_data, db)


def get_person_subject_by_person_id_and_subject_id_svc(
    person_id: int, subject_id: int, db: Session
):
    return PersonSubjectDAO.get_person_subject_by_person_id_and_subject_id(
        person_id, subject_id, db
    )
