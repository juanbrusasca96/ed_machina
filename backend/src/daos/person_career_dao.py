from models.person_career import PersonCareerModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from daos.DAO import DAO


class PersonCareerDAO(DAO):
    def __init__(self):
        super().__init__(PersonCareerModel, "person_career_id")

    def get_person_career_by_person_id_and_career_id(
        self, person_id: int, career_id: int, db: Session
    ):
        sql = text(
            """
            SELECT *
            FROM person_career
            WHERE person_id = :person_id
            AND career_id = :career_id
            """
        )

        result = db.execute(
            sql, {"person_id": person_id, "career_id": career_id}
        ).fetchone()

        if result:
            result = result._asdict()

        return result
