import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from models.career import CareerModel
from models.person_career import PersonCareerModel
from models.person_subject import PersonSubjectModel
from models.subject import SubjectModel
from models.person import PersonModel
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


def test_get_all_persons_with_related_data(test_db_setup, mocker):
    db = next(get_test_db())

    person1 = PersonModel(
        person_name="John",
        person_last_name="Doe",
        person_email="john.doe@example.com",
        person_phone="1234567890",
        person_address="Testing",
    )
    person2 = PersonModel(
        person_name="Jane",
        person_last_name="Smith",
        person_email="jane.smith@example.com",
        person_phone="0987654321",
        person_address="Testing 2",
    )
    db.add_all([person1, person2])
    db.commit()

    career1 = CareerModel(career_id=1, career_name="Engineering")
    career2 = CareerModel(career_id=2, career_name="Biology")
    db.add_all([career1, career2])
    db.commit()

    subject1 = SubjectModel(subject_id=1, subject_name="Math")
    subject2 = SubjectModel(subject_id=2, subject_name="Chemistry")
    db.add_all([subject1, subject2])
    db.commit()

    person_career1 = PersonCareerModel(
        person_id=person1.person_id, career_id=career1.career_id, enrollment_year=2021
    )
    person_career2 = PersonCareerModel(
        person_id=person2.person_id, career_id=career2.career_id, enrollment_year=2021
    )
    db.add_all([person_career1, person_career2])
    db.commit()

    person_subject1 = PersonSubjectModel(
        person_id=person1.person_id,
        subject_id=subject1.subject_id,
        study_time=5,
        subject_attempts=1,
    )
    person_subject2 = PersonSubjectModel(
        person_id=person2.person_id,
        subject_id=subject2.subject_id,
        study_time=5,
        subject_attempts=1,
    )
    db.add_all([person_subject1, person_subject2])
    db.commit()

    response = client.get("/front/person/get_all?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["persons"]) == 2
    assert data["persons"][0]["person_name"] == "John"
    assert data["persons"][0]["careers"] == [
        {"person_id": 1, "career_name": "Engineering"}
    ]
    assert data["persons"][0]["subjects"] == [{"person_id": 1, "subject_name": "Math"}]
    assert data["persons"][1]["person_name"] == "Jane"
    assert data["persons"][1]["careers"] == [{"person_id": 2, "career_name": "Biology"}]
    assert data["persons"][1]["subjects"] == [
        {"person_id": 2, "subject_name": "Chemistry"}
    ]


def test_get_all_persons_no_related_data(test_db_setup, mocker):
    db = next(get_test_db())

    person1 = PersonModel(
        person_name="Alice",
        person_last_name="Johnson",
        person_email="alice.johnson@example.com",
        person_phone="5555555555",
        person_address="Test Address",
    )
    db.add(person1)
    db.commit()

    mocker.patch("services.front.career_svc.get_related_careers_svc", return_value=[])
    mocker.patch("services.front.subject_svc.get_related_subjects_svc", return_value=[])

    response = client.get("/front/person/get_all?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["persons"]) == 1
    assert data["persons"][0]["person_name"] == "Alice"
    assert data["persons"][0]["careers"] == []
    assert data["persons"][0]["subjects"] == []


def test_get_all_persons_pagination(test_db_setup):
    db = next(get_test_db())

    for i in range(15):
        person = PersonModel(
            person_name=f"Person",
            person_last_name=f"LastName",
            person_email=f"person{i}@example.com",
            person_phone=f"1234567{i}",
            person_address=f"Address {i}",
        )
        db.add(person)
    db.commit()

    response = client.get("/front/person/get_all?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["persons"]) == 10

    response = client.get("/front/person/get_all?skip=10&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["persons"]) == 5


def test_get_all_persons_empty(test_db_setup):
    response = client.get("/front/person/get_all?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["persons"]) == 0
    assert data["total_rows"] == 0


def test_get_all_persons_invalid_skip_limit(test_db_setup):
    response = client.get("/front/person/get_all?skip=-1&limit=-5")
    assert response.status_code == 400


def test_get_all_persons_skip_zero_limit_zero(test_db_setup):
    db = next(get_test_db())

    person1 = PersonModel(
        person_name="John",
        person_last_name="Doe",
        person_email="john.doe@example.com",
        person_phone="1234567890",
        person_address="Testing",
    )
    person2 = PersonModel(
        person_name="Jane",
        person_last_name="Smith",
        person_email="jane.smith@example.com",
        person_phone="0987654321",
        person_address="Testing 2",
    )
    db.add_all([person1, person2])
    db.commit()

    response = client.get("/front/person/get_all?skip=0&limit=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["persons"]) == 0
    assert data["total_rows"] == 0


def test_get_all_persons_skip_greater_than_total(test_db_setup):
    db = next(get_test_db())

    person1 = PersonModel(
        person_name="John",
        person_last_name="Doe",
        person_email="john.doe@example.com",
        person_phone="1234567890",
        person_address="Testing",
    )
    person2 = PersonModel(
        person_name="Jane",
        person_last_name="Smith",
        person_email="jane.smith@example.com",
        person_phone="0987654321",
        person_address="Testing 2",
    )
    db.add_all([person1, person2])
    db.commit()

    response = client.get("/front/person/get_all?skip=10&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["persons"]) == 0
    assert data["total_rows"] == 0


def test_get_all_persons_large_limit(test_db_setup):
    db = next(get_test_db())

    person1 = PersonModel(
        person_name="John",
        person_last_name="Doe",
        person_email="john.doe@example.com",
        person_phone="1234567890",
        person_address="Testing",
    )
    person2 = PersonModel(
        person_name="Jane",
        person_last_name="Smith",
        person_email="jane.smith@example.com",
        person_phone="0987654321",
        person_address="Testing 2",
    )
    db.add_all([person1, person2])
    db.commit()

    response = client.get("/front/person/get_all?skip=0&limit=100")
    assert response.status_code == 200
    data = response.json()
    assert len(data["persons"]) == 2
    assert data["total_rows"] == 2


def test_sql_injection_attempt_get_all(test_db_setup):
    db = next(get_test_db())

    malicious_skip = "0; DROP TABLE person; --"
    malicious_limit = "10; DROP TABLE person; --"

    response = client.get(
        f"/front/person/get_all?skip={malicious_skip}&limit={malicious_limit}"
    )

    assert response.status_code == 422
    inspector = inspect(db.get_bind())
    assert (
        "person" in inspector.get_table_names()
    ), "La tabla 'person' debería existir; la inyección SQL no debe tener éxito."
