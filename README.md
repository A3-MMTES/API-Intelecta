# API Intelecta

Esta é uma API construída com FastAPI para o sistema Intelecta. Ela gerencia usuários, autenticação, turmas, matrículas, notas e muito mais.

## Funcionalidades Principais

A API é dividida em vários módulos para organizar as funcionalidades:

*   **Autenticação (`auth`):**
    *   Login de usuários com verificação de credenciais.
    *   Geração e validação de tokens de acesso (JWT).

*   **Gerenciamento de Usuários (`users`):**
    *   Listar, criar, deletar e atualizar usuários.
    *   Os usuários podem visualizar seus próprios dados.
    *   Controle de acesso baseado em cargos (roles).

*   **Segurança (`security` e `roles`):**
    *   Hashing de senhas para armazenamento seguro.
    *   Verificação de senhas.
    *   Um sistema de cargos para restringir o acesso a rotas específicas, garantindo que apenas usuários autorizados (como administradores) possam realizar certas operações.

## Testes

O projeto possui uma suíte de testes robusta para garantir a qualidade e a segurança do código.

### Boas Práticas Implementadas
1.  **Isolamento**: Cada teste utiliza um banco de dados em memória, garantindo que os testes não interfiram uns com os outros.
2.  **Fixtures Reutilizáveis**: Dados de teste são definidos em fixtures para serem compartilhados entre diferentes testes.
3.  **Testes de Integração**: Testam os endpoints da API de ponta a ponta, simulando o uso real.
4.  **Testes Unitários**: Testam funções e lógicas de negócio de forma isolada.
5.  **Validação de Segurança**: Inclui testes para verificar a autenticação e autorização dos endpoints.

## Como Executar

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Execute a API com Uvicorn:**
    ```bash
    uvicorn main:app --reload
    ```
A API estará disponível em `http://127.0.0.1:8000`.
