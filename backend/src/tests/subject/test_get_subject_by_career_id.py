import pytest
from fastapi.testclient import TestClient
from models.career_subject import CareerSubjectModel
from models.career import CareerModel
from models.subject import SubjectModel
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


def test_get_subjects_by_career_cached(mocker, test_db_setup):
    mocker.patch(
        "routes.front.subject_router.get_cache",
        return_value=[{"subject_id": 1, "subject_name": "Math"}],
    )

    response = client.get("/front/subject/get_by_career/1")

    assert response.status_code == 200
    data = response.json()
    assert data["cached"] is True
    assert len(data["result"]) == 1
    assert data["result"][0]["subject_name"] == "Math"


def test_get_subjects_by_career_not_cached(mocker, test_db_setup):
    db = next(get_test_db())

    career = CareerModel(career_name="Engineering")
    subject1 = SubjectModel(subject_name="Math")
    subject2 = SubjectModel(subject_name="Physics")
    db.add_all([career, subject1, subject2])
    db.commit()

    db.add_all(
        [
            CareerSubjectModel(
                career_id=career.career_id, subject_id=subject1.subject_id
            ),
            CareerSubjectModel(
                career_id=career.career_id, subject_id=subject2.subject_id
            ),
        ]
    )
    db.commit()

    mocker.patch("routes.front.subject_router.get_cache", return_value=None)
    mocker.patch("routes.front.subject_router.set_cache", return_value=None)

    response = client.get(f"/front/subject/get_by_career/{career.career_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["cached"] is False
    assert len(data["result"]) == 2
    assert data["result"][0]["subject_name"] == "Math"
    assert data["result"][1]["subject_name"] == "Physics"


def test_get_subjects_by_career_no_subjects(mocker, test_db_setup):
    db = next(get_test_db())

    career = CareerModel(career_name="EmptyCareer")
    db.add(career)
    db.commit()

    mocker.patch("routes.front.subject_router.get_cache", return_value=None)
    mocker.patch("routes.front.subject_router.set_cache", return_value=None)

    response = client.get(f"/front/subject/get_by_career/{career.career_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["cached"] is False
    assert len(data["result"]) == 0


def test_get_subjects_by_career_response_structure(mocker, test_db_setup):
    mocker.patch(
        "routes.front.subject_router.get_cache",
        return_value=[{"subject_id": 1, "subject_name": "Math"}],
    )

    response = client.get("/front/subject/get_by_career/1")

    assert response.status_code == 200
    data = response.json()

    assert "result" in data
    assert "cached" in data
    assert isinstance(data["result"], list)
    assert isinstance(data["cached"], bool)
