import pytest
from sqlalchemy import inspect
from models.person import PersonModel
from main import app
from fastapi.testclient import TestClient
from database import get_test_db, test_engine, Base, get_db, TestingSessionLocal
from sqlalchemy.orm import Session


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


def test_get_person_existing(test_db_setup):
    db = next(get_test_db())

    person = PersonModel(
        person_name="John",
        person_last_name="Doe",
        person_email="john.doe@example.com",
        person_phone="1234567890",
        person_address="Testing",
    )
    db.add(person)
    db.commit()
    db.refresh(person)

    response = client.get(f"/front/person/get/{person.person_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["person_name"] == "John"
    assert data["person_last_name"] == "Doe"
    assert data["person_email"] == "john.doe@example.com"
    assert data["person_phone"] == "1234567890"
    assert data["person_address"] == "Testing"


def test_get_person_not_existing(test_db_setup):
    response = client.get("/front/person/get/9999")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Person not found"}


def test_get_person_invalid_id(test_db_setup):
    response = client.get("/front/person/get/abc")
    assert response.status_code == 422


def test_get_person_existing_with_related_data(test_db_setup, mocker):
    db = next(get_test_db())

    person = PersonModel(
        person_name="John",
        person_last_name="Doe",
        person_email="john.doe@example.com",
        person_phone="1234567890",
        person_address="Testing",
    )
    db.add(person)
    db.commit()
    db.refresh(person)

    mocker.patch(
        "services.front.person_svc.get_related_careers",
        return_value=[{"career_id": 1, "career_name": "Engineering"}],
    )
    mocker.patch(
        "services.front.person_svc.get_related_subjects",
        return_value=[{"subject_id": 1, "subject_name": "Math"}],
    )

    response = client.get(f"/front/person/get/{person.person_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["person_name"] == "John"
    assert data["person_last_name"] == "Doe"
    assert data["person_email"] == "john.doe@example.com"
    assert data["person_phone"] == "1234567890"
    assert data["person_address"] == "Testing"
    assert data["careers"] == [{"career_id": 1, "career_name": "Engineering"}]
    assert data["subjects"] == [{"subject_id": 1, "subject_name": "Math"}]


def test_get_person_existing_no_related_data(test_db_setup, mocker):
    db = next(get_test_db())

    person = PersonModel(
        person_name="Jane",
        person_last_name="Smith",
        person_email="jane.smith@example.com",
        person_phone="1234567890",
        person_address="Testing",
    )
    db.add(person)
    db.commit()
    db.refresh(person)

    mocker.patch("services.front.person_svc.get_related_careers", return_value=[])
    mocker.patch("services.front.person_svc.get_related_subjects", return_value=[])

    response = client.get(f"/front/person/get/{person.person_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["person_name"] == "Jane"
    assert data["person_last_name"] == "Smith"
    assert data["person_email"] == "jane.smith@example.com"
    assert data["person_phone"] == "1234567890"
    assert data["person_address"] == "Testing"
    assert data["careers"] == []
    assert data["subjects"] == []


def test_sql_injection_attempt(test_db_setup):
    db = next(get_test_db())

    malicious_id = "1; DROP TABLE person; --"

    response = client.get(f"/front/person/get/{malicious_id}")

    assert response.status_code == 422
    inspector = inspect(db.get_bind())
    assert (
        "person" in inspector.get_table_names()
    ), "La tabla 'person' debería existir; la inyección SQL no debe tener éxito."
