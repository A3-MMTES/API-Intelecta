import pytest
from fastapi import status
from datetime import date
import models

# Testes para o router de professores

def test_list_teachers_as_admin(client, auth_headers, test_teacher):
    """Testa listagem de professores como admin"""
    response = client.get(
        "/teachers/",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_create_teacher_as_admin(client, auth_headers, db_session):
    """Testa criação de professor como admin"""
    # Cria um usuário para ser o professor
    user = models.User(
        email="newteacher@example.com",
        name="New Teacher",
        hashed_password="hashed_password",
        role="teacher",
        is_active=True,
        school_id=1
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    teacher_data = {
        "user_id": user.id,
        "subject": "Química",
        "hire_date": date(2024, 5, 1).isoformat()
    }
    
    response = client.post(
        "/teachers/",
        json=teacher_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["subject"] == "Química"

def test_get_teacher_by_id_as_admin(client, auth_headers, test_teacher):
    """Testa buscar professor por ID como admin"""
    response = client.get(
        f"/teachers/{test_teacher.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["subject"] == "Matemática"

def test_update_teacher_as_admin(client, auth_headers, test_teacher):
    """Testa atualização de professor como admin"""
    updated_data = {
        "subject": "Física"
    }
    
    response = client.put(
        f"/teachers/{test_teacher.id}",
        json=updated_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["subject"] == "Física"

def test_delete_teacher_as_admin(client, auth_headers, test_teacher, db_session):
    """Testa deleção de professor como admin"""
    # Cria um professor temporário para deletar
    user = models.User(
        email="tempteacher@example.com",
        name="Temp Teacher",
        hashed_password="hashed_password",
        role="teacher",
        is_active=True,
        school_id=1
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    temp_teacher = models.Teacher(
        user_id=user.id,
        subject="História",
        hire_date=date(2024, 1, 1)
    )
    db_session.add(temp_teacher)
    db_session.commit()
    db_session.refresh(temp_teacher)
    
    response = client.delete(
        f"/teachers/{temp_teacher.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
