from fastapi import APIRouter
from routes.front.person_router import person_router


front_routes = APIRouter(
    prefix="/front",
    tags=["front"],
)

front_routes.include_router(person_router)