# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
import models
from utils.security import get_password_hash

# Banco em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    # Cria as tabelas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # INSERE OS USUÁRIOS DOS .feature AQUI MESMO (depois que a tabela existe!)
    users_data = [
        ("admin@example.com",   "admin123",   "admin"),
        ("teacher@example.com", "teacher123", "teacher"),
        ("student@example.com", "student123", "student"),
    ]
    
    for email, password, role in users_data:
        exists = db.query(models.User).filter(models.User.email == email).first()
        if not exists:
            db.add(models.User(
                email=email,
                name=f"{role.capitalize()} Test",
                hashed_password=get_password_hash(password),
                role=role,
                is_active=True,
                school_id=1
            ))
    db.commit()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Tokens prontos para os steps BDD
@pytest.fixture
def admin_token(client):
    r = client.post("/auth/token", data={"username": "admin@example.com", "password": "admin123"})
    return r.json()["access_token"]

@pytest.fixture
def teacher_token(client):
    r = client.post("/auth/token", data={"username": "teacher@example.com", "password": "teacher123"})
    return r.json()["access_token"]

@pytest.fixture
def student_token(client):
    r = client.post("/auth/token", data={"username": "student@example.com", "password": "student123"})
    return r.json()["access_token"]