from typing import cast
from daos.person_career_dao import PersonCareerDAO
from models.person_career import PersonCareerModel
from services.base_service import BaseService
from sqlalchemy.orm import Session


class PersonCareerService(BaseService[PersonCareerModel]):
    def __init__(self, db: Session):
        person_career_dao = PersonCareerDAO(db)
        super().__init__(person_career_dao)
        self.dao: PersonCareerDAO = cast(PersonCareerDAO, self.dao)
