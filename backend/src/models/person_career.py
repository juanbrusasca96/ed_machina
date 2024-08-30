from sqlalchemy import Column, Date, ForeignKey, Integer
from database import Base


class PersonCareer(Base):
    __tablename__ = "person_career"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.id"))
    career_id = Column(Integer, ForeignKey("career.id"))
    enrollment_year = Column(Date, nullable=False)