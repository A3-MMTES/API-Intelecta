# tests/step_defs/test_student_access_steps.py
from pytest_bdd import scenarios, given, when, then, parsers
from starlette.testclient import TestClient

# Carrega os cenários
scenarios("../features/student_access.feature")

# Step de autenticação
@given(parsers.parse('eu sou um usuário autenticado com o perfil "{role}"'), target_fixture="auth_headers")
def authenticated_user_with_role(client: TestClient, role: str):
    credentials = {
        "admin":   ("admin@example.com",   "admin123"),
        "teacher": ("teacher@example.com", "teacher123"),
        "student": ("student@example.com", "student123"),
    }
    email, password = credentials[role]
    response = client.post("/auth/token", data={"username": email, "password": password})
    assert response.status_code == 200, f"Falha ao logar como {role}: {response.json()}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Step que faz a requisição — OBRIGATÓRIO TER target_fixture="context"
@when(parsers.parse('eu faço uma requisição GET para "{path}"'), target_fixture="context")
def make_get_request(client: TestClient, path: str, auth_headers: dict):
    response = client.get(path, headers=auth_headers)
    return {"response": response}

# Verifica status
@then(parsers.parse('o status da resposta deve ser {status_code:d}'))
def check_status_code(context, status_code: int):
    assert context["response"].status_code == status_code

# Opcional: verifica mensagem de erro
@then(parsers.parse('a resposta deve conter o detalhe "{detail}"'))
def check_error_detail(context, detail: str):
    assert context["response"].json().get("detail") == detail