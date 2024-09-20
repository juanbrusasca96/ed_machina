from typing import cast
from daos.career_dao import CareerDAO
from models.career import CareerModel
from services.base_service import BaseService
from sqlalchemy.orm import Session


class CareerService(BaseService[CareerModel]):
    def __init__(self, db: Session):
        career_dao = CareerDAO(db)
        super().__init__(career_dao)
        self.dao: CareerDAO = cast(CareerDAO, self.dao)

    def get_related_careers(self, person_ids: tuple):
        return self.dao.get_related_careers(person_ids)
