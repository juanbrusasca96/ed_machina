from fastapi import FastAPI
from routes.data_routes import data_routes
from routes.front_routes import front_routes
from database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(front_routes)
app.include_router(data_routes)
