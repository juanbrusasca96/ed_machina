from sqlalchemy.orm import Session
from daos.person_dao import PersonDAO
from utils.functions import get_dict_from_list
from services.front.career_svc import get_related_careers_svc
from services.front.subject_svc import get_related_subjects_svc


def get_person_by_email_svc(email: str, db: Session):
    return PersonDAO.get_person_by_email(email, db)


def get_person_by_id_svc(person_id: int, db: Session):
    person = PersonDAO.get_person_by_id(person_id, db)
    if person:
        person_id = person.get("person_id")
        careers = get_related_careers_svc((person_id,), db)
        subjects = get_related_subjects_svc((person_id,), db)
        person["careers"] = careers
        person["subjects"] = subjects

    return person


def get_all_persons_svc(skip: int, limit: int, db: Session):
    persons = PersonDAO.get_all_persons(skip, limit, db)
    if persons:
        person_ids = tuple(person["person_id"] for person in persons)
        careers = get_dict_from_list(
            get_related_careers_svc(person_ids, db), "person_id"
        )
        subjects = get_dict_from_list(
            get_related_subjects_svc(person_ids, db), "person_id"
        )

        for person in persons:
            person_id = person.get("person_id")
            person["careers"] = careers.get(person_id, [])
            person["subjects"] = subjects.get(person_id, [])

    return persons


def create_person_svc(person_data: dict, db: Session):
    return PersonDAO.create_person(person_data, db)
