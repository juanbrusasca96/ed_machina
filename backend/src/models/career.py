from sqlalchemy import Column, Integer, String
from models.subject import SubjectModel
from models.career_subject import CareerSubjectModel
from database import Base
from sqlalchemy.orm import relationship


class CareerModel(Base):
    __tablename__ = "career"

    career_id = Column(Integer, primary_key=True, index=True)
    career_name = Column(String, nullable=False)
