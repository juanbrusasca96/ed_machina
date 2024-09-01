from sqlalchemy import Column, Integer, String
from database import Base


class SubjectModel(Base):
    __tablename__ = "subject"
    
    subject_id = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String, nullable=False)