from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from models.person import PersonModel
from schemas.person_schemas import PersonCreate
from models.person_career import PersonCareerModel


def create_person_career(person: PersonModel, person_data: PersonCreate, db: Session):
    person_career = PersonCareerModel(
        person_id=person.get("person_id"), **person_data.career.model_dump()
    )
    db.add(person_career)
    db.commit()


def update_person_career(person_career, person_data: PersonCreate, db: Session):
    sql = text(
        """
        UPDATE person_career
        SET enrollment_year = :enrollment_year
        WHERE person_career_id = :person_career_id
        """
    )

    db.execute(
        sql,
        {
            "enrollment_year": person_data.career.enrollment_year,
            "person_career_id": person_career.get("person_career_id"),
        },
    )


def get_person_career_by_person_id_and_career_id(
    person_id: int, career_id: int, db: Session
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
