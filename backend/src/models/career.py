from sqlalchemy import Column, Integer, String
from database import Base


class CareerModel(Base):
    __tablename__ = "career"

    career_id = Column(Integer, primary_key=True, index=True)
    career_name = Column(String, nullable=False)
