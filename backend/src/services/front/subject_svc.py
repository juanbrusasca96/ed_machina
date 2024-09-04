from sqlalchemy.orm import Session
from daos.subject_dao import SubjectDAO

subject_dao = SubjectDAO()


def get_subjects_by_career_id(career_id: int, db: Session):
    return subject_dao.get_subjects_by_career_id(career_id, db)


def get_related_subjects_svc(person_ids: tuple, db: Session):
    return subject_dao.get_related_subjects(person_ids, db)
