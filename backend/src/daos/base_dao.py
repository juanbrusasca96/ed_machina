from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import Type, TypeVar, Generic, Optional, List, Dict, Any

T = TypeVar("T")


class BaseDAO(Generic[T]):
    def __init__(self, model: Type[T], id_name: str, db: Session):
        self.model = model
        self.id_name = id_name
        self.db = db

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, self.id_name) == entity_id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        query = (
            self.db.query(self.model)
            .order_by(getattr(self.model, self.id_name))
            .offset(skip)
        )

        if limit == -1:
            return query.all()

        return query.limit(limit).all()

    def create(self, entity_data: dict) -> T:
        entity = self.model(**entity_data)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity_id: int, update_data: dict) -> Optional[T]:
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        for key, value in update_data.items():
            setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True

    def get_by_field(self, field_name: str, value) -> Optional[T]:
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, field_name) == value)
            .first()
        )

    def get_by_fields(self, filters: dict) -> Optional[T]:
        query = self.db.query(self.model)
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.first()

    def get_all_by_field(
        self, field_name: str, value, skip: int = 0, limit: int = 10
    ) -> List[T]:
        query = (
            self.db.query(self.model)
            .filter(getattr(self.model, field_name) == value)
            .order_by(getattr(self.model, self.id_name))
            .offset(skip)
        )
        if limit == -1:
            return query.all()
        return query.limit(limit).all()

    def count(self) -> int:
        return self.db.query(self.model).count()

    def count_by_field(self, field_name: str, value) -> int:
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, field_name) == value)
            .count()
        )

    def exists_by_id(self, entity_id: int) -> bool:
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, self.id_name) == entity_id)
            .first()
            is not None
        )

    def exists_by_field(self, field_name: str, value) -> bool:
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, field_name) == value)
            .first()
            is not None
        )

    def delete_by_field(self, field_name: str, value) -> bool:
        entities = self.db.query(self.model).filter(
            getattr(self.model, field_name) == value
        )
        if entities.count() == 0:
            return False
        entities.delete(synchronize_session=False)
        self.db.commit()
        return True

    def update_fields(self, entity_id: int, update_data: dict) -> Optional[T]:
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        for key, value in update_data.items():
            setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def filter(self, filters: dict, skip: int = 0, limit: int = 10) -> List[T]:
        query = self.db.query(self.model)
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        query = query.order_by(getattr(self.model, self.id_name)).offset(skip)
        if limit == -1:
            return query.all()
        return query.limit(limit).all()

    def get_all_ordered(
        self, order_by: str, asc: bool = True, skip: int = 0, limit: int = 10
    ) -> List[T]:
        order = getattr(self.model, order_by)
        if not asc:
            order = order.desc()
        query = self.db.query(self.model).order_by(order).offset(skip)
        if limit == -1:
            return query.all()
        return query.limit(limit).all()

    def get_by_like(
        self, field_name: str, value: str, skip: int = 0, limit: int = 10
    ) -> List[T]:
        query = (
            self.db.query(self.model)
            .filter(getattr(self.model, field_name).like(f"%{value}%"))
            .order_by(getattr(self.model, self.id_name))
            .offset(skip)
        )
        if limit == -1:
            return query.all()
        return query.limit(limit).all()
