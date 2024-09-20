from daos.base_dao import BaseDAO
from models.career_subject import CareerSubjectModel
from sqlalchemy.orm import Session


class CareerSubjectDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(
            CareerSubjectModel, CareerSubjectModel.career_subject_id.name, db
        )
