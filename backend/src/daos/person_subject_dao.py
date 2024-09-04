from models.person_subject import PersonSubjectModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from daos.DAO import DAO


class PersonSubjectDAO(DAO):
    def __init__(self):
        super().__init__(PersonSubjectModel, "person_subject_id")

    @classmethod
    def get_person_subject_by_person_id_and_subject_id(
        self, person_id: int, subject_id: int, db: Session
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
