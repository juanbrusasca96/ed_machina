from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from schemas.person_schemas import PersonCreate


def get_career_by_id(person_data: PersonCreate, db: Session):
    sql = text(
        """
        SELECT c.*, s.*, cs.*
        FROM career c
        JOIN career_subject cs ON c.career_id = cs.career_id
        JOIN subject s ON cs.subject_id = s.subject_id
        WHERE c.career_id = :career_id
        AND s.subject_id = :subject_id
        """
    )

    result = db.execute(
        sql,
        {
            "career_id": person_data.career.career_id,
            "subject_id": person_data.subject.subject_id,
        },
    )

    result = result.fetchone()
    if result:
        result = result._asdict()

    return result
