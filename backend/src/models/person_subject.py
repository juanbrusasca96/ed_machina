from sqlalchemy import Column, Float, ForeignKey, Integer
from database import Base


class PersonSubject(Base):
    __tablename__ = "person_subject"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.id"), index=True)
    subject_id = Column(Integer, ForeignKey("subject.id"), index=True)
    study_time = Column(Float, nullable=False)
    subject_attempts = Column(Integer, nullable=False)