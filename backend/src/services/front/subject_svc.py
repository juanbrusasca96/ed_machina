from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_subjects_by_career_id(career_id: int, db: Session):
    sql = text(
        """
        SELECT s.*
        FROM subject s
        JOIN career_subject cs ON s.subject_id = cs.subject_id
        WHERE cs.career_id = :career_id
        """
    )

    result = db.execute(sql, {"career_id": career_id}).fetchall()
    if result:
        result = [row._asdict() for row in result]

    return result