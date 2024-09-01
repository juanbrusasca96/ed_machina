from pydantic import BaseModel, EmailStr, field_validator, Field
from schemas.person_career_schemas import PersonCareer
from schemas.person_subject_schemas import PersonSubject


class Person(BaseModel):
    person_name: str = Field(min_length=3, max_length=50)
    person_last_name: str = Field(min_length=3, max_length=50)
    person_email: EmailStr
    person_address: str = Field(min_length=5, max_length=100)
    person_phone: str = Field(pattern=r"^\+?\d{7,15}$")

    @field_validator("person_name", "person_last_name")
    def validate_names(cls, v):
        if not v.isalpha():
            raise ValueError("Name and last name should only contain letters.")
        return v

    @field_validator("person_phone")
    def validate_phone(cls, v):
        if not v.startswith("+") and len(v) > 10:
            raise ValueError(
                'Phone numbers longer than 10 digits must start with a "+" sign.'
            )
        return v


class PersonCreate(Person):
    career: PersonCareer
    subject: PersonSubject


class PersonCreateResponse(Person):
    person_id: int

    class ConfigDict:
        orm_mode = True


class PersonResponse(PersonCreateResponse):
    careers: list[dict]
    subjects: list[dict]
