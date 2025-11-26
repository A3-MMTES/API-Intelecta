import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from main import app
from models import User
from database import get_db
from utils.security import get_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Cenários
scenarios('../features/auth.feature')

@pytest.fixture
def test_client(db_session): # depend on db_session to ensure mocks are set up
    return TestClient(app)

@pytest.fixture
def db_session(mocker):
    db = []
    # This is a very simplistic mock. It might need to be more sophisticated.
    def mock_get_db():
        # This is a mock session object with a query method.
        session = mocker.Mock()
        def query(model):
            # mock filter().first()
            q = mocker.Mock()
            def filter(criterion):
                # very basic filter implementation for these tests
                email = criterion.right.value
                user = next((u for u in db if u.email == email), None)
                q.first.return_value = user
                return q
            q.filter = filter
            return q
        session.query = query
        def add(item):
            db.append(item)
        session.add = add
        def commit():
            pass
        session.commit = commit
        def refresh(item):
            pass
        session.refresh = refresh

        yield session

    mocker.patch('routers.auth.get_db', mock_get_db)
    mocker.patch('utils.security.get_db', mock_get_db)

    return db

@given('um usuário com o email "admin@example.com" e senha "admin123" existe')
def create_admin_user(client):
    engine = client.app.dependency_overrides[get_db]().bind
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    if not db.query(User).filter(User.email == "admin@example.com").first():
        user = User(
            email="admin@example.com",
            name="Admin Test",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True,
            school_id=1
        )
        db.add(user)
        db.commit()
    db.close()

@when(parsers.parse('eu faço uma requisição POST para "{path}" com o email "{email}" e senha "{password}"'))
def make_login_request(test_client, path, email, password):
    test_client.response = test_client.post(path, data={"username": email, "password": password})

@then(parsers.parse('o status da resposta deve ser {status_code:d}'))
def check_status_code(test_client, status_code):
    assert test_client.response.status_code == status_code

@then(parsers.parse('a resposta deve conter um "{key}"'))
def check_response_key(test_client, key):
    assert key in test_client.response.json()

@then(parsers.parse('a resposta deve conter o detalhe "{detail}"'))
def check_response_detail(test_client, detail):
    assert test_client.response.json()["detail"] == detail
