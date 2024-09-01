from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from utils.functions import get_dict_from_list
from services.front.person_career_svc import create_person_career
from services.front.person_subject_svc import create_person_subject
from models.person import PersonModel
from schemas.person_schemas import PersonCreate


def get_person_by_email(email: str, db: Session):
    email = email.strip().lower() if email else None
    sql = text(
        """
        SELECT *
        FROM person
        WHERE person_email = :email
        """
    )

    result = db.execute(sql, {"email": email}).fetchone()

    if result:
        result = result._asdict()

    return result


def get_person_by_id(person_id: int, db: Session):
    sql_person = text(
        """
        SELECT *
        FROM person
        WHERE person_id = :person_id
        """
    )
    person_result = db.execute(sql_person, {"person_id": person_id}).fetchone()
    if not person_result:
        return None

    person = person_result._asdict()
    person_id = person.get("person_id")

    careers = get_related_careers((person_id,), db)
    subjects = get_related_subjects((person_id,), db)

    person["careers"] = careers
    person["subjects"] = subjects

    return person


def get_all_persons(skip: int, limit: int, db: Session):
    sql_persons = text(
        """
        SELECT *
        FROM person
        LIMIT :limit OFFSET :skip
        """
    )
    persons_result = db.execute(sql_persons, {"limit": limit, "skip": skip}).fetchall()

    if not persons_result:
        return []

    persons = [row._asdict() for row in persons_result]
    person_ids = tuple(person["person_id"] for person in persons)

    careers = get_dict_from_list(get_related_careers(person_ids, db), "person_id")
    subjects = get_dict_from_list(get_related_subjects(person_ids, db), "person_id")

    for person in persons:
        person_id = person.get("person_id")
        person["careers"] = careers.get(person_id, [])
        person["subjects"] = subjects.get(person_id, [])

    return persons


def get_related_careers(person_ids: tuple, db: Session):
    sql_careers = text(
        """
        SELECT c.career_name, pc.person_id
        FROM career c
        JOIN person_career pc ON c.career_id = pc.career_id
        WHERE pc.person_id IN :person_ids
        """
    )
    careers_result = db.execute(sql_careers, {"person_ids": person_ids}).fetchall()
    return [row._asdict() for row in careers_result]


def get_related_subjects(person_ids: tuple, db: Session):
    sql_subjects = text(
        """
        SELECT s.subject_name, ps.person_id
        FROM subject s
        JOIN person_subject ps ON s.subject_id = ps.subject_id
        WHERE ps.person_id IN :person_ids
        """
    )
    subjects_result = db.execute(sql_subjects, {"person_ids": person_ids}).fetchall()
    return [row._asdict() for row in subjects_result]


def create_person(person_data: dict, db: Session):
    person_data.get("person_email").strip().lower()
    person_db = PersonModel(**person_data)
    db.add(person_db)
    db.commit()
    db.refresh(person_db)

    return person_db
