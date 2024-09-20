from typing import cast
from daos.career_subject_dao import CareerSubjectDAO
from models.career_subject import CareerSubjectModel
from services.base_service import BaseService
from sqlalchemy.orm import Session


class CareerSubjectService(BaseService[CareerSubjectModel]):
    def __init__(self, db: Session):
        career_subject_dao = CareerSubjectDAO(db)
        super().__init__(career_subject_dao)
        self.dao: CareerSubjectDAO = cast(CareerSubjectDAO, self.dao)
