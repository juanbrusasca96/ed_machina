import pytest
from fastapi.testclient import TestClient
from models.career import CareerModel
from database import get_test_db, test_engine, Base, get_db, TestingSessionLocal
from main import app

app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db_setup():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    Base.metadata.create_all(bind=test_engine)

    connection = test_engine.connect()
    transaction = connection.begin()
    TestingSessionLocal.configure(bind=connection)

    yield

    transaction.rollback()
    connection.close()

    Base.metadata.drop_all(bind=test_engine)
    TestingSessionLocal.close_all()


def test_get_all_careers_route_cached(mocker, test_db_setup):
    mocker.patch(
        "routes.front.career_router.get_cache",
        return_value=[{"career_id": 1, "career_name": "Engineering"}],
    )

    response = client.get("/front/career/get_all")

    assert response.status_code == 200
    data = response.json()
    assert data["cached"] is True
    assert len(data["result"]) == 1
    assert data["result"][0]["career_name"] == "Engineering"


def test_get_all_careers_route_not_cached(mocker, test_db_setup):
    db = next(get_test_db())

    career1 = CareerModel(career_name="Engineering")
    career2 = CareerModel(career_name="Biology")
    db.add_all([career1, career2])
    db.commit()

    mocker.patch("routes.front.career_router.get_cache", return_value=None)

    mocker.patch("routes.front.career_router.set_cache", return_value=None)

    response = client.get("/front/career/get_all")

    assert response.status_code == 200
    data = response.json()
    assert data["cached"] is False
    assert len(data["result"]) == 2
    assert data["result"][0]["career_name"] == "Engineering"
    assert data["result"][1]["career_name"] == "Biology"


def test_get_all_careers_route_response_structure(mocker, test_db_setup):

    mocker.patch(
        "routes.front.career_router.get_cache",
        return_value=[{"career_id": 1, "career_name": "Engineering"}],
    )

    response = client.get("/front/career/get_all")

    assert response.status_code == 200
    data = response.json()

    assert "result" in data
    assert "cached" in data
    assert isinstance(data["result"], list)
    assert isinstance(data["cached"], bool)
