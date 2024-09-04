from sqlalchemy.orm import Session
from daos.person_career_dao import PersonCareerDAO
from models.person import PersonModel
from schemas.person_schemas import PersonCreate


def create_person_career_svc(
    person: PersonModel, person_data: PersonCreate, db: Session
):
    PersonCareerDAO.create_person_career(person, person_data, db)


def update_person_career_svc(person_career, person_data: PersonCreate, db: Session):
    PersonCareerDAO.update_person_career(person_career, person_data, db)


def get_person_career_by_person_id_and_career_id_svc(
    person_id: int, career_id: int, db: Session
):
    return PersonCareerDAO.get_person_career_by_person_id_and_career_id(
        person_id, career_id, db
    )
