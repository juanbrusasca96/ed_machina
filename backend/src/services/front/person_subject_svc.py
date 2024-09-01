from sqlalchemy import text
from models.person import PersonModel
from schemas.person_schemas import PersonCreate
from models.person_subject import PersonSubjectModel
from sqlalchemy.orm import Session


def create_person_subject(person: PersonModel, person_data: PersonCreate, db: Session):
    person_subject = PersonSubjectModel(
        person_id=person.get("person_id"), **person_data.subject.model_dump()
    )
    db.add(person_subject)
    db.commit()


def update_person_subject(person_subject, person_data: PersonCreate, db: Session):
    sql = text(
        """
        UPDATE person_subject
        SET study_time = :study_time,
            subject_attempts = :subject_attempts
        WHERE person_subject_id = :person_subject_id
        """
    )

    db.execute(
        sql,
        {
            "study_time": person_subject.get("study_time") + person_data.subject.study_time,
            "subject_attempts": person_subject.get("subject_attempts")
            + person_data.subject.subject_attempts,
            "person_subject_id": person_subject.get("person_subject_id"),
        },
    )


def get_person_subject_by_person_id_and_subject_id(
    person_id: int, subject_id: int, db: Session
):
    sql = text(
        """
        SELECT *
        FROM person_subject
        WHERE person_id = :person_id
        AND subject_id = :subject_id
        """
    )

    result = db.execute(
        sql, {"person_id": person_id, "subject_id": subject_id}
    ).fetchone()

    if result:
        result = result._asdict()

    return result
