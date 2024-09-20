from typing import cast
from daos.subject_dao import SubjectDAO
from models.subject import SubjectModel
from services.base_service import BaseService
from sqlalchemy.orm import Session


class SubjectService(BaseService[SubjectModel]):
    def __init__(self, db: Session):
        subject_dao = SubjectDAO(db)
        super().__init__(subject_dao)
        self.dao: SubjectDAO = cast(SubjectDAO, self.dao)

    def get_subjects_by_career_id(self, career_id: int):
        return self.dao.get_subjects_by_career_id(career_id)

    def get_related_subjects(self, person_ids: tuple):
        return self.dao.get_related_subjects(person_ids)
