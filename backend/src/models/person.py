from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship, Mapped
from models.career import CareerModel
from models.person_career import PersonCareerModel
from models.subject import SubjectModel
from models.person_subject import PersonSubjectModel


class PersonModel(Base):
    __tablename__ = "person"

    person_id = Column(Integer, primary_key=True, index=True)
    person_name = Column(String, nullable=False)
    person_last_name = Column(String, nullable=False)
    person_email = Column(String, unique=True)
    person_address = Column(String, nullable=False)
    person_phone = Column(String, nullable=False)

    careers: Mapped[list[CareerModel]] = relationship(
        CareerModel, secondary=PersonCareerModel.__tablename__, lazy="joined"
    )
    subjects: Mapped[list[SubjectModel]] = relationship(
        SubjectModel, secondary=PersonSubjectModel.__tablename__, lazy="joined"
    )
