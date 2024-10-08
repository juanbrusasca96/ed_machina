from sqlalchemy import Column, ForeignKey, Integer
from database import Base


class PersonCareerModel(Base):
    __tablename__ = "person_career"

    person_career_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    career_id = Column(Integer, ForeignKey("career.career_id"))
    enrollment_year = Column(Integer, nullable=False)
