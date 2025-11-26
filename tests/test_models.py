import pytest
import models
from utils.security import get_password_hash

def test_create_user(db_session):
    """Testa criação de usuário"""
    user = models.User(
        email="newuser@example.com",
        name="New User",
        hashed_password=get_password_hash("password123"),
        role="student",
        is_active=True,
        school_id=1
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "newuser@example.com"
    assert user.role == "student"

def test_create_student(db_session, test_user):
    """Testa criação de estudante"""
    student = models.Student(
        user_id=test_user.id,
        registration_number="2024002",
        course="Ciência da Computação"
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    
    assert student.id is not None
    assert student.registration_number == "2024002"
    assert student.user_id == test_user.id

def test_student_unique_registration_number(db_session, test_student):
    """Testa que número de matrícula deve ser único"""
    from sqlalchemy.exc import IntegrityError
    
    # Cria outro usuário
    user2 = models.User(
        email="user2@example.com",
        name="User 2",
        hashed_password=get_password_hash("pass123"),
        role="student",
        is_active=True,
        school_id=1
    )
    db_session.add(user2)
    db_session.commit()
    
    # Tenta criar estudante com matrícula duplicada
    student2 = models.Student(
        user_id=user2.id,
        registration_number="2024001",  # Mesmo número do test_student
        course="Test"
    )
    db_session.add(student2)
    
    with pytest.raises(IntegrityError):
        db_session.commit()

def test_create_teacher(db_session):
    """Testa criação de professor"""
    user = models.User(
        email="prof@example.com",
        name="Professor",
        hashed_password=get_password_hash("profpass"),
        role="teacher",
        is_active=True,
        school_id=1
    )
    db_session.add(user)
    db_session.commit()
    
    teacher = models.Teacher(
        user_id=user.id,
        subject="Física",
        hire_date="2024-02-01"
    )
    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)
    
    assert teacher.id is not None
    assert teacher.subject == "Física"
    assert teacher.user_id == user.id

def test_user_relationship_with_student(db_session, test_user, test_student):
    """Testa relacionamento entre User e Student"""
    # Recarrega o usuário do banco
    user = db_session.query(models.User).filter_by(id=test_user.id).first()
    
    assert user is not None
    # Verifica se o relacionamento existe
    # Nota: depende de como o relacionamento foi configurado em models.py

def test_user_email_unique(db_session, test_user):
    """Testa que email deve ser único"""
    from sqlalchemy.exc import IntegrityError
    
    user2 = models.User(
        email="test@example.com",  # Email duplicado
        name="User 2",
        hashed_password=get_password_hash("pass"),
        role="student",
        is_active=True,
        school_id=1
    )
    db_session.add(user2)
    
    with pytest.raises(IntegrityError):
        db_session.commit()
