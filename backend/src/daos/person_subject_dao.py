from models.person_subject import PersonSubjectModel
from sqlalchemy.orm import Session
from daos.base_dao import BaseDAO


class PersonSubjectDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(
            PersonSubjectModel, PersonSubjectModel.person_subject_id.name, db
        )
