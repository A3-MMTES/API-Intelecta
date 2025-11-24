import pytest
from fastapi import status

def test_login_success(client, test_user):
    """Testa login bem-sucedido"""
    response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    """Testa login com senha incorreta"""
    response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_nonexistent_user(client):
    """Testa login com usuário inexistente"""
    response = client.post(
        "/login",
        data={
            "username": "nonexistent@example.com",
            "password": "anypassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_inactive_user(client, db_session, test_user):
    """Testa login com usuário inativo"""
    test_user.is_active = False
    db_session.commit()
    
    response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_access_token():
    """Testa criação de token de acesso"""
    from routers.auth import create_access_token
    from datetime import timedelta
    
    data = {"sub": "1", "role": "admin"}
    token = create_access_token(data=data)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_access_token():
    """Testa verificação de token"""
    from routers.auth import create_access_token, verify_access_token
    
    data = {"sub": "1", "role": "admin"}
    token = create_access_token(data=data)
    
    payload = verify_access_token(token)
    assert payload is not None
    assert payload["sub"] == "1"

def test_verify_invalid_token():
    """Testa verificação de token inválido"""
    from routers.auth import verify_access_token
    
    invalid_token = "invalid.token.here"
    payload = verify_access_token(invalid_token)
    
    assert payload is None
