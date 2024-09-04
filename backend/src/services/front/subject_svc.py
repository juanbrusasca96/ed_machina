from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from daos.subject_dao import SubjectDAO


def get_subjects_by_career_id(career_id: int, db: Session):
    return SubjectDAO.get_subjects_by_career_id(career_id, db)


def get_related_subjects_svc(person_ids: tuple, db: Session):
    return SubjectDAO.get_related_subjects(person_ids, db)
