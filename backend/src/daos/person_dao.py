from sqlalchemy.orm import Session
from daos.base_dao import BaseDAO
from models.person import PersonModel


class PersonDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(PersonModel, PersonModel.person_id.name, db)
