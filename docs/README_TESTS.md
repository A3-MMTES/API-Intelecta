# Guia de Testes Automatizados - Projeto Intelecta

Este documento serve como guia completo para a suíte de testes automatizados do projeto **Intelecta**. O objetivo é garantir a qualidade, estabilidade e segurança da API, com uma cobertura de código mínima de **70%** aplicada em todo o projeto.

## 🚀 Como Executar os Testes

A maneira mais simples de rodar a suíte de testes completa e gerar o relatório de cobertura é utilizando o script `RUN_TESTS.sh`.

```bash
./RUN_TESTS.sh
```

Este script executa o `pytest`, mede a cobertura dos testes e falhará se a cobertura total for inferior a 70%. Ao final, ele exibirá um relatório de cobertura no terminal e gerará um relatório HTML detalhado.

### Visualizando o Relatório de Cobertura

Para uma análise mais detalhada das linhas de código cobertas, abra o relatório HTML gerado.

```bash
# O comando pode variar dependendo do seu sistema operacional
open htmlcov/index.html
```

## 🏗️ Estrutura dos Testes

Os testes estão organizados no diretório `tests/` e seguem uma estrutura lógica que espelha a arquitetura da aplicação.

```
tests/
├── __init__.py
├── conftest.py              # Fixtures e configurações globais de teste
├── test_models.py           # Testes unitários para os modelos de dados (SQLAlchemy)
├── routers/
│   ├── __init__.py
│   ├── test_auth.py         # Testes de integração para autenticação e autorização
│   ├── test_students.py     # Testes para os endpoints de estudantes
│   └── test_classes.py      # Testes para os endpoints de turmas
└── utils/
    ├── __init__.py
    ├── test_security.py     # Testes unitários para funções de segurança (hashing, JWT)
    └── test_roles.py        # Testes unitários para o controle de acesso (RBAC)
```

## 🎯 Cobertura de Testes

A suíte de testes abrange as áreas mais críticas da aplicação, garantindo que a lógica de negócio, segurança e endpoints funcionem como esperado.

| Módulo | Cobertura |
|---------------------|-----------|
| `routers/auth.py` | ~90% |
| `utils/security.py` | ~95% |
| `utils/roles.py` | ~100% |
| `models.py` | ~70% |
| `routers/students.py` | ~75% |
| `routers/classes.py` | ~75% |

### Funcionalidades Cobertas

-   **Autenticação e Segurança:**
    -   Login com credenciais válidas e inválidas.
    -   Geração e validação de tokens JWT.
    -   Hashing e verificação de senhas.
    -   Proteção de rotas contra acesso anônimo.

-   **Controle de Acesso (RBAC):**
    -   Validação de permissões por perfil (`admin`, `teacher`, `student`).
    -   Bloqueio de endpoints para perfis não autorizados.

-   **Modelos de Dados:**
    -   Criação de entidades (`User`, `Student`, etc.).
    -   Validação de `constraints` do banco de dados (ex: email único).
    -   Relacionamentos entre tabelas.

-   **Endpoints da API (CRUD):**
    -   Criação, leitura, atualização e exclusão de recursos (ex: estudantes, turmas).
    -   Tratamento de erros e validações de entrada.

## 🧰 Fixtures de Teste (`conftest.py`)

Para facilitar a escrita de testes e evitar duplicação de código, a suíte utiliza um conjunto de *fixtures* reutilizáveis, disponíveis em `tests/conftest.py`.

-   `db_session`: Fornece uma sessão de banco de dados SQLite em memória, garantindo o isolamento total entre os testes.
-   `client`: Um cliente de teste do FastAPI para fazer requisições à API.
-   `test_user`, `test_student`, `test_teacher`: Usuários pré-configurados com diferentes perfis para testes de autenticação e autorização.
-   `auth_headers`: Cabeçalhos HTTP com um token de autenticação válido para acessar rotas protegidas.

## ✨ Boas Práticas e Ferramentas

-   **Isolamento:** Cada teste é executado em uma transação de banco de dados separada que é revertida ao final, garantindo que não haja interferência entre eles.
-   **Testes de Integração e Unitários:** A suíte combina testes unitários (para funções específicas) e de integração (para endpoints completos da API).
-   **Configuração Centralizada:** O arquivo `pytest.ini` define as configurações do `pytest`, incluindo o nível mínimo de cobertura e os formatos dos relatórios.
-   **Dependências de Desenvolvimento:** As dependências necessárias para os testes estão listadas em `requirements-dev.txt`.
