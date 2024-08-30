from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from config.environment import *
from config.prod import *
import os



DOCKER_DATABASE_URL = os.getenv(enviro.DB)

if DOCKER_DATABASE_URL:
    engine = create_engine(DOCKER_DATABASE_URL)
else:
    engine = create_engine(enviro.SQL_DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()