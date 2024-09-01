import pytest
from main import app
from fastapi.testclient import TestClient
from services.front.person_svc import get_person_by_email
from models.person import PersonModel
from sqlalchemy.orm import Session
from database import get_db, get_test_db, test_engine, Base

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db_setup():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    yield
    with test_engine.connect() as connection:
        for tbl in reversed(Base.metadata.sorted_tables):
            connection.execute(tbl.delete())


def test_get_person_by_email():
    db: Session = next(get_test_db())
    email = "test@example.com"

    new_person = PersonModel(
        person_name="Test",
        person_last_name="Test",
        person_email=email,
        person_phone="1234567890",
        person_address="Test",
    )
    db.add(new_person)
    db.commit()

    person = get_person_by_email(email, db)
    assert person is not None
    assert person.get("person_email") == email

    db.delete(new_person)
    db.commit()


def test_get_person_by_email_not_found():
    db: Session = next(get_test_db())

    email = "nonexistent@example.com"

    person = get_person_by_email(email, db)
    assert person is None


def test_get_person_by_email_none():
    db: Session = next(get_test_db())

    email = None
    person = get_person_by_email(email, db)
    assert person is None


def test_get_person_by_email_with_spaces():
    db: Session = next(get_test_db())

    email = "test@example.com"
    new_person = PersonModel(
        person_name="Test",
        person_last_name="Test",
        person_email=email,
        person_phone="1234567890",
        person_address="Test",
    )
    db.add(new_person)
    db.commit()

    person = get_person_by_email("  test@example.com  ", db)
    assert person is not None
    assert person.get("person_email") == email

    db.delete(new_person)
    db.commit()


def test_sql_injection_attempt():
    db: Session = next(get_test_db())

    email = "test@example.com' OR '1'='1"
    person = get_person_by_email(email, db)
    assert person is None


def test_case_sensitivity():
    db: Session = next(get_test_db())

    email = "test@example.com"
    new_person = PersonModel(
        person_name="Test",
        person_last_name="Test",
        person_email=email,
        person_phone="1234567890",
        person_address="Test",
    )
    db.add(new_person)
    db.commit()

    person = get_person_by_email("TEST@EXAMPLE.COM", db)
    assert person is not None
    assert person.get("person_email") == email

    db.delete(new_person)
    db.commit()


def test_check_email_exists_route():
    db: Session = next(get_test_db())
    email = "test@example.com"
    new_person = PersonModel(
        person_name="Test",
        person_last_name="Test",
        person_email=email,
        person_phone="1234567890",
        person_address="Test",
    )
    db.add(new_person)
    db.commit()
    response = client.get(f"/front/person/check_email_exists?email={email}")
    assert response.status_code == 200
    assert response.json() is True
    db.delete(new_person)
    db.commit()


def test_check_email_does_not_exist_route():
    email = "nonexistent@example.com"
    response = client.get(f"/front/person/check_email_exists?email={email}")
    assert response.status_code == 200
    assert response.json() is False


def test_invalid_email_format():
    email = "invalid-email-format"
    response = client.get(f"/front/person/check_email_exists?email={email}")
    assert response.status_code == 422


def test_empty_email():
    email = ""
    response = client.get(f"/front/person/check_email_exists?email={email}")
    assert response.status_code == 422
