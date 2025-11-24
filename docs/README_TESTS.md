# Documentação de Testes - Projeto Intelecta

## Cobertura de Testes: >= 70%

### Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartilhadas
├── test_models.py           # Testes dos modelos ORM
├── routers/
│   ├── __init__.py
│   ├── test_auth.py         # Testes de autenticação
│   ├── test_students.py     # Testes do router de estudantes
│   └── test_classes.py      # Testes do router de classes
└── utils/
    ├── __init__.py
    ├── test_security.py     # Testes de segurança
    └── test_roles.py        # Testes de controle de acesso
```

### Como Executar os Testes

1. **Instalar dependências de teste:**
```bash
pip install -r requirements-dev.txt
```

2. **Executar todos os testes:**
```bash
pytest
```

3. **Executar com cobertura:**
```bash
pytest --cov=. --cov-report=html
```

4. **Ver relatório de cobertura:**
```bash
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html # Windows
```

### Áreas Cobertas pelos Testes

#### 1. Autenticação (test_auth.py)
- Login bem-sucedido
- Login com senha incorreta
- Login com usuário inexistente
- Login com usuário inativo
- Criação de tokens JWT
- Verificação de tokens válidos/inválidos

#### 2. Segurança (test_security.py)
- Hash de senhas
- Verificação de senhas corretas/incorretas
- Criação de tokens com expiração padrão/customizada
- Validação de tokens JWT

#### 3. Controle de Acesso (test_roles.py)
- Verificação de permissões por role (admin, teacher, student)
- Bloqueio de acesso não autorizado
- Múltiplos roles permitidos

#### 4. Modelos (test_models.py)
- Criação de usuários
- Criação de estudantes
- Criação de professores
- Validação de constraints (único email, único número de matrícula)
- Relacionamentos entre entidades

#### 5. Router de Estudantes (test_students.py)
- Criação de estudantes (admin)
- Listagem de estudantes
- Busca por ID
- Atualização
- Deleção
- Validação de matrícula duplicada
- Proteção de endpoints (requer autenticação)

#### 6. Router de Classes (test_classes.py)
- Listagem de classes (admin e teacher)
- Criação de classes
- Bloqueio de acesso para students
- Proteção de endpoints

### Fixtures Disponíveis (conftest.py)

- `db_session`: Sessão de banco de dados em memória
- `client`: Cliente de teste FastAPI
- `test_user`: Usuário admin de teste
- `test_student`: Estudante de teste
- `test_teacher`: Professor de teste
- `auth_token`: Token de autenticação válido
- `auth_headers`: Headers HTTP com token

### Métricas de Cobertura

O pytest está configurado para:
- Falhar se a cobertura for menor que 70%
- Gerar relatórios em HTML, terminal e XML
- Mostrar linhas não cobertas

### Boas Práticas Implementadas

1. **Isolação**: Cada teste usa banco em memória isolado
2. **Fixtures reutilizáveis**: Dados de teste compartilhados
3. **Testes de integração**: Testam endpoints completos
4. **Testes unitários**: Testam funções individuais
5. **Validação de segurança**: Testes de autenticação e autorização

