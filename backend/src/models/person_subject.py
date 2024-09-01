from sqlalchemy import Column, Float, ForeignKey, Integer
from database import Base


class PersonSubjectModel(Base):
    __tablename__ = "person_subject"
    
    person_subject_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id"), index=True)
    subject_id = Column(Integer, ForeignKey("subject.subject_id"), index=True)
    study_time = Column(Float, nullable=False)
    subject_attempts = Column(Integer, nullable=False)