from sqlalchemy import Column, Integer, String
from database import Base


class Career(Base):
    __tablename__ = "career"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)