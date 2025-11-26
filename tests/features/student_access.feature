# tests/features/student_access.feature
Feature: Controle de Acesso para a Rota de Estudantes
  Como um usuário autenticado
  Eu quero ter acesso à lista de estudantes apenas se eu tiver o perfil correto
  Para garantir a segurança e a privacidade dos dados

  Scenario: Administrador acessa a lista de estudantes com sucesso
    Given eu sou um usuário autenticado com o perfil "admin"
    When eu faço uma requisição GET para "/students/"
    Then o status da resposta deve ser 200

  Scenario: Professor acessa a lista de estudantes com sucesso
    Given eu sou um usuário autenticado com o perfil "teacher"
    When eu faço uma requisição GET para "/students/"
    Then o status da resposta deve ser 200

  Scenario: Estudante é bloqueado de acessar a lista de estudantes
    Given eu sou um usuário autenticado com o perfil "student"
    When eu faço uma requisição GET para "/students/"
    Then o status da resposta deve ser 403
    And a resposta deve conter o detalhe "You don't have permission to access this resource"

  Scenario: Estudante é bloqueado de acessar a lista de estudantes
  Given eu sou um usuário autenticado com o perfil "student"
  When eu faço uma requisição GET para "/students/"
  Then o status da resposta deve ser 403
  And a resposta deve conter o detalhe "Acesso negado: permissão insuficiente"
