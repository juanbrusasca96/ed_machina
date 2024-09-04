from sqlalchemy.orm import Session
from daos.career_dao import CareerDAO
from schemas.person_schemas import PersonCreate

career_dao = CareerDAO()

def get_career_by_id_svc(person_data: PersonCreate, db: Session):
    return career_dao.get_by_id(db, person_data.career.career_id)


def get_all_careers_svc(db: Session):
    return career_dao.get_all(db)


def get_related_careers_svc(person_ids: list, db: Session):
    return career_dao.get_related_careers(person_ids, db)
