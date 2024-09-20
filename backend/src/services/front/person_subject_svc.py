from typing import cast
from daos.person_subject_dao import PersonSubjectDAO
from models.person_subject import PersonSubjectModel
from services.base_service import BaseService
from sqlalchemy.orm import Session


class PersonSubjectService(BaseService[PersonSubjectModel]):
    def __init__(self, db: Session):
        person_subject_dao = PersonSubjectDAO(db)
        super().__init__(person_subject_dao)
        self.dao: PersonSubjectDAO = cast(PersonSubjectDAO, self.dao)
