from sqlalchemy import text
from sqlalchemy.orm import Session


class SubjectDAO:
    @staticmethod
    def get_related_subjects(person_ids: tuple, db: Session):
        sql_subjects = text(
            """
            SELECT s.subject_name, ps.person_id
            FROM subject s
            JOIN person_subject ps ON s.subject_id = ps.subject_id
            WHERE ps.person_id IN :person_ids
            """
        )
        subjects_result = db.execute(
            sql_subjects, {"person_ids": person_ids}
        ).fetchall()
        return [row._asdict() for row in subjects_result]

    @staticmethod
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
