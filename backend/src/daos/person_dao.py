from sqlalchemy import text
from sqlalchemy.orm import Session
from daos.DAO import DAO
from models.person import PersonModel


class PersonDAO(DAO):
    def __init__(self):
        super().__init__(PersonModel, "person_id")

    def get_person_by_email(self, email: str, db: Session):
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
