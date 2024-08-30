from sqlalchemy import Column, ForeignKey, Integer
from database import Base


class CareerSubject(Base):
    __tablename__ = "career_subject"
    
    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("career.id"), index=True)
    subject_id = Column(Integer, ForeignKey("subject.id"), index=True)
    