import pytest
from fastapi import HTTPException, status
from unittest.mock import MagicMock, patch
from auth_utils import get_current_user
from models import User

# Mock para o token scheme
@pytest.fixture
def mock_oauth2_scheme():
    return MagicMock(return_value="mock_token")

# Mock para a função verify_access_token
@pytest.fixture
def mock_verify_access_token():
    with patch('auth_utils.verify_access_token') as mock:
        yield mock

# Mock para a sessão do banco de dados
@pytest.fixture
def mock_db_session():
    return MagicMock()

def test_get_current_user_invalid_token(mock_oauth2_scheme, mock_verify_access_token, mock_db_session):
    """Testa get_current_user com token inválido (payload None)"""
    mock_verify_access_token.return_value = None
    
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token=mock_oauth2_scheme(), db=mock_db_session)
        
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_no_sub_in_payload(mock_oauth2_scheme, mock_verify_access_token, mock_db_session):
    """Testa get_current_user com payload sem 'sub'"""
    mock_verify_access_token.return_value = {"role": "admin"}
    
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token=mock_oauth2_scheme(), db=mock_db_session)
        
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_user_not_found(mock_oauth2_scheme, mock_verify_access_token, mock_db_session):
    """Testa get_current_user com usuário não encontrado no banco"""
    mock_verify_access_token.return_value = {"sub": "1", "role": "admin"}
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token=mock_oauth2_scheme(), db=mock_db_session)
        
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_success(mock_oauth2_scheme, mock_verify_access_token, mock_db_session):
    """Testa get_current_user com sucesso"""
    mock_verify_access_token.return_value = {"sub": "1", "role": "admin"}
    mock_user = User(id=1, email="test@example.com", name="Test User", hashed_password="hashed", role="admin", school_id=1)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    user = get_current_user(token=mock_oauth2_scheme(), db=mock_db_session)
    
    assert user == mock_user
