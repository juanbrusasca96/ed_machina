from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.redis_cache import get_cache, set_cache
from services.front.subject_svc import SubjectService
from database import get_db


subject_router = APIRouter(
    prefix="/subject",
    tags=["Subject"],
)


@subject_router.get("/get_by_career/{career_id}")
async def get_subjects_by_career_route(career_id: int, db: Session = Depends(get_db)):
    cache_key = f"get_subjects_by_career_{career_id}"
    cache_result = get_cache(cache_key)
    if cache_result:
        return {"result": cache_result, "cached": True}
    
    subject_service = SubjectService(db)
    result_dict = subject_service.get_subjects_by_career_id(career_id)
    set_cache(cache_key, result_dict, 900) # 15 minutes
    
    return {"result": result_dict, "cached": False}