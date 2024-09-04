from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.front.subject_svc import get_subjects_by_career_id
from database import get_db


subject_router = APIRouter(
    prefix="/subject",
    tags=["Subject"],
)


@subject_router.get("/get_by_career/{career_id}")
async def get_subjects_by_career_route(career_id: int, db: Session = Depends(get_db)):
    return get_subjects_by_career_id(career_id, db)