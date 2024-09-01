from sqlalchemy import Column, ForeignKey, Integer
from database import Base


class CareerSubjectModel(Base):
    __tablename__ = "career_subject"
    
    career_subject_id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("career.career_id"), index=True)
    subject_id = Column(Integer, ForeignKey("subject.subject_id"), index=True)
    