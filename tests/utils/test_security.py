import pytest
from datetime import timedelta

def test_get_password_hash():
    """Testa hash de senha"""
    from utils.security import get_password_hash
    
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed is not None
    assert hashed != password
    assert len(hashed) > 0

def test_verify_password_correct():
    """Testa verificação de senha correta"""
    from utils.security import get_password_hash, verify_password
    
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    """Testa verificação de senha incorreta"""
    from utils.security import get_password_hash, verify_password
    
    password = "testpassword123"
    wrong_password = "wrongpassword"
    hashed = get_password_hash(password)
    
    assert verify_password(wrong_password, hashed) is False

def test_create_access_token_default_expiry():
    """Testa criação de token com expiração padrão"""
    from utils.security import create_access_token
    
    data = {"sub": "1", "role": "admin"}
    token = create_access_token(data=data)
    
    assert token is not None
    assert isinstance(token, str)

def test_create_access_token_custom_expiry():
    """Testa criação de token com expiração customizada"""
    from utils.security import create_access_token
    
    data = {"sub": "1", "role": "admin"}
    expires_delta = timedelta(minutes=60)
    token = create_access_token(data=data, expires_delta=expires_delta)
    
    assert token is not None
    assert isinstance(token, str)

def test_verify_access_token_valid():
    """Testa verificação de token válido"""
    from utils.security import create_access_token, verify_access_token
    
    data = {"sub": "123", "role": "teacher"}
    token = create_access_token(data=data)
    
    payload = verify_access_token(token)
    
    assert payload is not None
    assert payload["sub"] == "123"
    assert payload["role"] == "teacher"

def test_verify_access_token_invalid():
    """Testa verificação de token inválido"""
    from utils.security import verify_access_token
    
    invalid_token = "this.is.invalid"
    payload = verify_access_token(invalid_token)
    
    assert payload is None

# def test_get_current_user_with_valid_token(client, test_user, auth_headers):
#     """Testa obtenção de usuário atual com token válido"""
#     # Este teste será implementado quando tivermos um endpoint que use get_current_user
#     pass
