# tests/features/auth.feature
Feature: Autenticação de Usuário
  Como um usuário do sistema
  Eu quero me autenticar para acessar recursos protegidos
  E garantir que usuários não autorizados sejam bloqueados

  Scenario: Login com sucesso
    Given um usuário com o email "admin@example.com" e senha "admin123" existe
    When eu faço uma requisição POST para "/auth/token" com o email "admin@example.com" e senha "admin123"
    Then o status da resposta deve ser 200
    And a resposta deve conter um "access_token"

  Scenario: Login com senha incorreta
    When eu faço uma requisição POST para "/auth/token" com o email "admin@example.com" e senha "wrongpassword"
    Then o status da resposta deve ser 401
    And a resposta deve conter o detalhe "Incorrect username or password"
