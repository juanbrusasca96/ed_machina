from sqlalchemy.orm import Session
from daos.career_dao import CareerDAO
from schemas.person_schemas import PersonCreate


def get_career_by_id_svc(person_data: PersonCreate, db: Session):
    return CareerDAO.get_career_by_id(person_data, db)


def get_all_careers_svc(db: Session):
    return CareerDAO.get_all_careers(db)


def get_related_careers_svc(person_ids: tuple, db: Session):
    return CareerDAO.get_related_careers(person_ids, db)
