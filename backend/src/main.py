from fastapi import FastAPI
from routes.front_routes import front_routes
from database import Base, engine
from models import person_career, subject, career_subject, career, person, person_subject


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(front_routes)