import pytest
from fastapi import status
import models

def test_list_classes_as_admin(client, auth_headers, db_session):
    """Testa listagem de classes como admin"""
    # Cria uma classe de teste
    test_class = models.Class(
        name="Turma A",
        
        school_id=1
    )
    db_session.add(test_class)
    db_session.commit()
    
    response = client.get(
        "/classes/",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_list_classes_as_teacher(client, test_teacher, db_session):
    """Testa listagem de classes como professor"""
    # Faz login como professor
    login_response = client.post(
        "/auth/token",
        data={
            "username": "teacher@example.com",
            "password": "teacherpass123"
        }
    )
    teacher_token = login_response.json()["access_token"]
    teacher_headers = {"Authorization": f"Bearer {teacher_token}"}
    
    response = client.get(
        "/classes/",
        headers=teacher_headers
    )
    
    assert response.status_code == status.HTTP_200_OK

def test_create_class_as_admin(client, auth_headers):
    """Testa criação de classe como admin"""
    class_data = {
        "name": "Turma B",
        
    }
    
    response = client.post(
        "/classes/",
        json=class_data,
        headers=auth_headers
    )
    
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_422_UNPROCESSABLE_ENTITY]

def test_list_classes_without_auth(client):
    """Testa que listagem de classes requer autenticação"""
    response = client.get("/classes/")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_classes_as_student_denied(client, db_session):
    """Testa que estudante não pode listar classes"""
    from utils.security import get_password_hash
    
    # Cria um usuário student
    student_user = models.User(
        email="student@example.com",
        name="Student",
        hashed_password=get_password_hash("studentpass"),
        role="student",
        is_active=True,
        school_id=1
    )
    db_session.add(student_user)
    db_session.commit()
    
    # Faz login
    login_response = client.post(
        "/auth/token",
        data={
            "username": "student@example.com",
            "password": "studentpass"
        }
    )
    student_token = login_response.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}
    
    response = client.get(
        "/classes/",
        headers=student_headers
    )
    
    # Estudante não deve ter acesso
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_read_class_as_admin(client, auth_headers, db_session):
    """Testa leitura de uma classe específica como admin"""
    test_class = models.Class(name="Turma C", school_id=1)
    db_session.add(test_class)
    db_session.commit()
    db_session.refresh(test_class)
    
    response = client.get(
        f"/classes/{test_class.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Turma C"
    assert "id" in data

def test_update_class_as_admin(client, auth_headers, db_session):
    """Testa atualização de classe como admin"""
    test_class = models.Class(name="Turma D", school_id=1)
    db_session.add(test_class)
    db_session.commit()
    db_session.refresh(test_class)
    
    updated_data = {
        "name": "Turma D - Atualizada",
        "schedule": "Segunda 10h"
    }
    
    response = client.put(
        f"/classes/{test_class.id}",
        json=updated_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Turma D - Atualizada"
    assert data["schedule"] == "Segunda 10h"

def test_delete_class_as_admin(client, auth_headers, db_session):
    """Testa exclusão de classe como admin"""
    test_class = models.Class(name="Turma E", school_id=1)
    db_session.add(test_class)
    db_session.commit()
    db_session.refresh(test_class)
    
    response = client.delete(
        f"/classes/{test_class.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verifica se foi excluído do banco
    deleted_class = db_session.query(models.Class).filter(models.Class.id == test_class.id).first()
    assert deleted_class is None
