from fastapi import APIRouter
from routes.front.person_router import person_router
from routes.front.career_router import career_router
from routes.front.subject_router import subject_router


front_routes = APIRouter(
    prefix="/front"
)

front_routes.include_router(person_router)
front_routes.include_router(career_router)
front_routes.include_router(subject_router)
