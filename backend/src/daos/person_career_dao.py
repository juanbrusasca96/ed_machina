from models.person_career import PersonCareerModel
from sqlalchemy.orm import Session
from daos.base_dao import BaseDAO


class PersonCareerDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(PersonCareerModel, PersonCareerModel.person_career_id.name, db)
