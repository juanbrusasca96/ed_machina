from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.front.career_svc import get_all_careers
from database import get_db


career_router = APIRouter(
    prefix="/career",
    tags=["Career"],
)


@career_router.get("/get_all")
async def get_all_careers_route(db: Session = Depends(get_db)):
    return get_all_careers(db)
