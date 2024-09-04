from fastapi import FastAPI
from routes.data_routes import data_routes
from routes.front_routes import front_routes
from database import Base, engine, test_engine
from fastapi.middleware.cors import CORSMiddleware
from config.prod import *


Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=test_engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=enviro.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["filename"]
)


app.include_router(front_routes)
app.include_router(data_routes)
