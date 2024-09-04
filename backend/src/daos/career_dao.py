from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from models.career import CareerModel
from daos.DAO import DAO


class CareerDAO(DAO):
    def __init__(self):
        super().__init__(CareerModel, "career_id")
    
    def get_related_careers(self, person_ids: tuple, db: Session):
        sql_careers = text(
            """
            SELECT c.career_name, pc.person_id, pc.enrollment_year
            FROM career c
            JOIN person_career pc ON c.career_id = pc.career_id
            WHERE pc.person_id IN :person_ids
            """
        )
        careers_result = db.execute(sql_careers, {"person_ids": person_ids}).fetchall()
        return [row._asdict() for row in careers_result]
