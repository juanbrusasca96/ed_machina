from sqlalchemy import text
from sqlalchemy.orm import Session
from models.person import PersonModel


class PersonDAO:
    @staticmethod
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

    @staticmethod
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

        return person

    @staticmethod
    def get_all_persons(skip: int, limit: int, db: Session):
        sql_persons = text(
            """
            SELECT *
            FROM person
            LIMIT :limit OFFSET :skip
            """
        )
        persons_result = db.execute(
            sql_persons, {"limit": limit, "skip": skip}
        ).fetchall()

        if not persons_result:
            return []

        persons = [row._asdict() for row in persons_result]

        return persons
    
    @staticmethod
    def create_person(person_data: dict, db: Session):
        person_data.get("person_email").strip().lower()
        person_db = PersonModel(**person_data)
        db.add(person_db)
        db.commit()
        db.refresh(person_db)

        return person_db
