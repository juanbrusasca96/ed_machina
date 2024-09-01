from pydantic import BaseModel


class PersonSubject(BaseModel):
    study_time: float
    subject_attempts: int
    subject_id: int
