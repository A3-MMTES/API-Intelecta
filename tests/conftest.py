import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
import models

# Banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco de dados para cada teste"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Cria um cliente de teste FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """Cria um usuário de teste"""
    from utils.security import get_password_hash
    
    user = models.User(
        email="test@example.com",
        name="Test User",
        hashed_password=get_password_hash("testpassword123"),
        role="admin",
        is_active=True,
        school_id=1
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_student(db_session, test_user):
    """Cria um estudante de teste"""
    student = models.Student(
        user_id=test_user.id,
        registration_number="2024001",
        course="Engenharia de Software"
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    return student

@pytest.fixture
def test_teacher(db_session):
    """Cria um professor de teste"""
    from utils.security import get_password_hash
    
    user = models.User(
        email="teacher@example.com",
        name="Test Teacher",
        hashed_password=get_password_hash("teacherpass123"),
        role="teacher",
        is_active=True,
        school_id=1
    )
    db_session.add(user)
    db_session.commit()
    
    teacher = models.Teacher(
        user_id=user.id,
        subject="Matemática",
        hire_date="2024-01-01"
    )
    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)
    return teacher

@pytest.fixture
def auth_token(client, test_user):
    """Obtém um token de autenticação"""
    response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    """Retorna headers com token de autenticação"""
    return {"Authorization": f"Bearer {auth_token}"}
