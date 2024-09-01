from os import getcwd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from sqlalchemy.sql import text
from sqlalchemy import inspect


upload_router = APIRouter(
    prefix="/upload",
)


@upload_router.post("/")
async def upload_data(db: Session = Depends(get_db)):
    name = "cargas"
    ext = "sql"
    file = getcwd() + f"/config/sql/{name}.{ext}"

    insp = inspect(engine)
    for table in insp.get_table_names():
        db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
    with open(file, "r", encoding="utf-8") as f:
        data = f.read()
        db.execute(text(data))

    return {"message": "Data uploaded successfully"}
