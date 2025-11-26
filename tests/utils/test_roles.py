import pytest
from utils.roles import require_role
from fastapi import HTTPException
import models

@pytest.mark.skip(reason="Testes de roles com decoradores requerem contexto HTTP completo")
def test_require_role_decorator_admin_access(client, test_user, auth_headers):
    """Testa acesso de admin com decorador require_role"""
    pass

@pytest.mark.skip(reason="Implementar quando tivermos endpoint real que use roles")
def test_require_role_decorator_student_access(client, test_user):
    """Testa bloqueio de estudante para rota admin"""
    pass

