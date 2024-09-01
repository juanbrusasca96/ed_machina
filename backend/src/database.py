from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.prod import *
import os



DOCKER_DATABASE_URL = os.getenv(enviro.DB)

if DOCKER_DATABASE_URL:
    engine = create_engine(DOCKER_DATABASE_URL)
else:
    engine = create_engine(enviro.SQL_DATABASE_URL)
    
test_engine = create_engine(enviro.SQL_TEST_DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


Base = declarative_base()


def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
        
def get_test_db():
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()