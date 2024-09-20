from typing import Generic, List, Optional, TypeVar
from daos.base_dao import BaseDAO


T = TypeVar("T")


class BaseService(Generic[T]):
    def __init__(self, dao: BaseDAO[T]):
        self.dao = dao

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self.dao.get_by_id(entity_id)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        return self.dao.get_all(skip, limit)

    def create(self, entity_data: dict) -> T:
        return self.dao.create(entity_data)

    def update(self, entity_id: int, update_data: dict) -> Optional[T]:
        return self.dao.update(entity_id, update_data)

    def delete(self, entity_id: int) -> bool:
        return self.dao.delete(entity_id)

    def get_by_field(self, field_name: str, value) -> Optional[T]:
        return self.dao.get_by_field(field_name, value)

    def get_by_fields(self, filters: dict) -> Optional[T]:
        return self.dao.get_by_fields(filters)

    def get_all_by_field(
        self, field_name: str, value, skip: int = 0, limit: int = 10
    ) -> List[T]:
        return self.dao.get_all_by_field(field_name, value, skip, limit)

    def count(self) -> int:
        return self.dao.count()

    def count_by_field(self, field_name: str, value) -> int:
        return self.dao.count_by_field(field_name, value)

    def exists_by_id(self, entity_id: int) -> bool:
        return self.dao.exists_by_id(entity_id)

    def exists_by_field(self, field_name: str, value) -> bool:
        return self.dao.exists_by_field(field_name, value)

    def delete_by_field(self, field_name: str, value) -> bool:
        return self.dao.delete_by_field(field_name, value)

    def update_fields(self, entity_id: int, update_data: dict) -> Optional[T]:
        return self.dao.update_fields(entity_id, update_data)

    def filter(self, filters: dict, skip: int = 0, limit: int = 10) -> List[T]:
        return self.dao.filter(filters, skip, limit)

    def get_all_ordered(self, order_by: str, skip: int = 0, limit: int = 10) -> List[T]:
        return self.dao.get_all_ordered(order_by, skip, limit)

    def get_by_like(
        self, field_name: str, value: str, skip: int = 0, limit: int = 10
    ) -> List[T]:
        return self.dao.get_by_like(field_name, value, skip, limit)
