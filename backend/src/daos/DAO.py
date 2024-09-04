from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import Type, TypeVar, Generic, Optional, List, Dict, Any

T = TypeVar("T")


class DAO(Generic[T]):
    def __init__(self, model: Type[T], id_name: str):
        self.model = model
        self.id_name = id_name

    def get_by_id(self, db: Session, entity_id: int) -> Optional[T]:
        return (
            db.query(self.model)
            .filter(getattr(self.model, self.id_name) == entity_id)
            .first()
        )

    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> List[T]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, entity_data: dict) -> T:
        entity = self.model(**entity_data)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def update(self, db: Session, entity_id: int, update_data: dict) -> Optional[T]:
        entity = self.get_by_id(db, entity_id)
        if not entity:
            return None
        for key, value in update_data.items():
            setattr(entity, key, value)
        db.commit()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, entity_id: int) -> bool:
        entity = self.get_by_id(db, entity_id)
        if not entity:
            return False
        db.delete(entity)
        db.commit()
        return True
