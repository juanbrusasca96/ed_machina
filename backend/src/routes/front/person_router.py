from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.front.person_svc import check_email_exists
from database import get_db
from pydantic import EmailStr


person_router = APIRouter(
    prefix="/person",
)


@person_router.get("/check_email_exists")
async def check_email_exists_function(email: EmailStr, db: Session = Depends(get_db)):
    return check_email_exists(email, db)