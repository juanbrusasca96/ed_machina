from sqlalchemy import text
from sqlalchemy.orm import Session
from models.subject import SubjectModel
from daos.base_dao import BaseDAO


class SubjectDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(SubjectModel, SubjectModel.subject_id.name, db)

    def get_related_subjects(self, person_ids: tuple):
        sql_subjects = text(
            """
            SELECT s.subject_name, ps.person_id, ps.study_time, ps.subject_attempts
            FROM subject s
            JOIN person_subject ps ON s.subject_id = ps.subject_id
            WHERE ps.person_id IN :person_ids
            """
        )
        subjects_result = self.db.execute(
            sql_subjects, {"person_ids": person_ids}
        ).fetchall()
        return [row._asdict() for row in subjects_result]

    def get_subjects_by_career_id(self, career_id: int):
        sql = text(
            """
            SELECT s.*
            FROM subject s
            JOIN career_subject cs ON s.subject_id = cs.subject_id
            WHERE cs.career_id = :career_id
            """
        )

        result = self.db.execute(sql, {"career_id": career_id}).fetchall()
        if result:
            result = [row._asdict() for row in result]

        return result
