from pydantic import BaseModel
from datetime import date


class PersonCareer(BaseModel):
    enrollment_year: int = date.today().year
    career_id: int
