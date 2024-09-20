from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.functions import to_dict
from utils.redis_cache import get_cache, set_cache
from services.front.career_svc import CareerService
from database import get_db


career_router = APIRouter(
    prefix="/career",
    tags=["Career"],
)


@career_router.get("/get_all")
async def get_all_careers_route(db: Session = Depends(get_db)):
    cache_key = "get_all_careers"
    cache_result = get_cache(cache_key)
    if cache_result:
        return {"result": cache_result, "cached": True}

    career_service = CareerService(db)

    result = career_service.get_all(limit=-1)
    result_dict = [to_dict(career) for career in result]
    set_cache(cache_key, result_dict, 900) # 15 minutes

    return {"result": result_dict, "cached": False}
