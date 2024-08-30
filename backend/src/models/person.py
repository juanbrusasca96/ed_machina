from sqlalchemy import Column, Integer, String
from database import Base


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)