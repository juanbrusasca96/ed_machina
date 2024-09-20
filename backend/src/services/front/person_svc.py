from typing import cast
from daos.person_dao import PersonDAO
from models.person import PersonModel
from services.base_service import BaseService
from sqlalchemy.orm import Session


class PersonService(BaseService[PersonModel]):
    def __init__(self, db: Session):
        person_dao = PersonDAO(db)
        super().__init__(person_dao)
        self.dao: PersonDAO = cast(PersonDAO, self.dao)
