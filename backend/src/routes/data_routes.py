from fastapi import APIRouter
from routes.data.upload_router import upload_router


data_routes = APIRouter(
    prefix="/data",
    tags=["data"],
)

data_routes.include_router(upload_router)
