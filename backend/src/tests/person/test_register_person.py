import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from models.subject import SubjectModel
from models.career_subject import CareerSubjectModel
from models.person import PersonModel
from models.career import CareerModel
from schemas.person_schemas import PersonCreate
from database import get_test_db, test_engine, Base, TestingSessionLocal, get_db
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


def test_register_person_new_successful(test_db_setup, mocker):
    db = next(get_test_db())
    person_data = PersonCreate(
        person_name="John",
        person_last_name="Doe",
        person_email="john.doe@example.com",
        person_phone="+1234567890",
        person_address="1234 Main St",
        career={"career_id": 1, "enrollment_year": 2021},
        subject={"subject_id": 1, "study_time": 5, "subject_attempts": 1},
    )

    db.add(CareerModel(career_id=1, career_name="Engineering"))
    db.add(SubjectModel(subject_id=1, subject_name="Math"))
    db.commit()
    db.add(CareerSubjectModel(career_id=1, subject_id=1))
    db.commit()

    mocker.patch(
        "services.front.career_svc.get_career_by_id",
        return_value={
            "career_id": 1,
            "career_name": "Engineering",
            "subject_name": "Math",
            "subject_id": 1,
            "career_subject_id": 1,
        },
    )
    mocker.patch("services.front.person_svc.get_person_by_email", return_value=None)
    mocker.patch(
        "services.front.person_svc.create_person",
        return_value=PersonModel(person_id=1, person_email="john.doe@example.com"),
    )

    response = client.post("/front/person/register", json=person_data.model_dump())

    data = response.json()
    assert data["message"] == "Person created successfully"
    assert response.status_code == 200
    assert data["person"]["person_email"] == "john.doe@example.com"


def test_register_person_career_not_found(test_db_setup, mocker):
    person_data = PersonCreate(
        person_name="Jane",
        person_last_name="Smith",
        person_email="jane.smith@example.com",
        person_phone="+1234567890",
        person_address="5678 Second St",
        career={"career_id": 2, "enrollment_year": 2021},
        subject={"subject_id": 2, "study_time": 5, "subject_attempts": 1},
    )

    mocker.patch("services.front.career_svc.get_career_by_id", return_value=None)

    response = client.post("/front/person/register", json=person_data.model_dump())

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Career not found or subject does not belong to career"


def test_register_person_update_career_and_subject(test_db_setup, mocker):
    db = next(get_test_db())
    person_data = PersonCreate(
        person_name="Alice",
        person_last_name="Johnson",
        person_email="alice.johnson@example.com",
        person_phone="+9876543210",
        person_address="7890 Third Blvd",
        career={"career_id": 1, "enrollment_year": 2021},
        subject={"subject_id": 1, "study_time": 5, "subject_attempts": 1},
    )

    db.add(CareerModel(career_id=1, career_name="Engineering"))
    db.add(SubjectModel(subject_id=1, subject_name="Math"))
    db.commit()
    db.add(CareerSubjectModel(career_id=1, subject_id=1))
    db.commit()

    mocker.patch(
        "services.front.career_svc.get_career_by_id",
        return_value={
            "career_id": 1,
            "career_name": "Engineering",
            "subject_name": "Math",
            "subject_id": 1,
            "career_subject_id": 1,
        },
    )
    mocker.patch(
        "services.front.person_svc.get_person_by_email",
        return_value=PersonModel(person_id=2, person_email="alice.johnson@example.com"),
    )
    mocker.patch(
        "services.front.person_career_svc.get_person_career_by_person_id_and_career_id",
        return_value={"person_career_id": 1},
    )
    mocker.patch(
        "services.front.person_subject_svc.get_person_subject_by_person_id_and_subject_id",
        return_value={"person_subject_id": 1},
    )
    mocker.patch(
        "services.front.person_career_svc.update_person_career", return_value=None
    )
    mocker.patch(
        "services.front.person_subject_svc.update_person_subject", return_value=None
    )

    response = client.post("/front/person/register", json=person_data.model_dump())

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Person created successfully"
    assert data["person"]["person_email"] == "alice.johnson@example.com"


def test_register_person_create_new_career_and_subject(test_db_setup, mocker):
    db = next(get_test_db())
    person_data = PersonCreate(
        person_name="Bob",
        person_last_name="Brown",
        person_email="bob.brown@example.com",
        person_phone="+1122334455",
        person_address="1357 Fifth Ave",
        career={"career_id": 1, "enrollment_year": 2021},
        subject={"subject_id": 1, "study_time": 5, "subject_attempts": 1},
    )

    db.add(CareerModel(career_id=1, career_name="Engineering"))
    db.add(SubjectModel(subject_id=1, subject_name="Math"))
    db.commit()
    db.add(CareerSubjectModel(career_id=1, subject_id=1))
    db.commit()

    mocker.patch(
        "services.front.career_svc.get_career_by_id",
        return_value={
            "career_id": 1,
            "career_name": "Engineering",
            "subject_name": "Math",
            "subject_id": 1,
            "career_subject_id": 1,
        },
    )
    mocker.patch(
        "services.front.person_svc.get_person_by_email",
        return_value=PersonModel(person_id=3, person_email="bob.brown@example.com"),
    )
    mocker.patch(
        "services.front.person_career_svc.get_person_career_by_person_id_and_career_id",
        return_value=None,
    )
    mocker.patch(
        "services.front.person_subject_svc.get_person_subject_by_person_id_and_subject_id",
        return_value=None,
    )
    mocker.patch(
        "services.front.person_career_svc.create_person_career", return_value=None
    )
    mocker.patch(
        "services.front.person_subject_svc.create_person_subject", return_value=None
    )

    response = client.post("/front/person/register", json=person_data.model_dump())

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Person created successfully"
    assert data["person"]["person_email"] == "bob.brown@example.com"


def test_register_person_invalid_data(test_db_setup):
    invalid_person_data = {
        "person_name": "Jo",
        "person_last_name": "Doe1",
        "person_email": "not-an-email",
        "person_phone": "12345",
        "person_address": "123",
        "career": {"career_id": 1, "enrollment_year": 2021},
        "subject": {"subject_id": 1, "study_time": 5, "subject_attempts": 1},
    }

    response = client.post("/front/person/register", json=invalid_person_data)

    assert response.status_code == 422


def test_sql_injection_attempt_register_person(test_db_setup):
    db = next(get_test_db())

    malicious_email = "'; DROP TABLE person; --"

    person_data = {
        "person_name": "John",
        "person_last_name": "Doe",
        "person_email": malicious_email,
        "person_phone": "1234567890",
        "person_address": "1234 Main St",
    }

    response = client.post("/front/person/register", json=person_data)

    assert response.status_code == 400 or response.status_code == 422
    inspector = inspect(db.get_bind())
    assert (
        "person" in inspector.get_table_names()
    ), "La tabla 'person' debería existir; la inyección SQL no debe tener éxito."
