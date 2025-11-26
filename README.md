
# Intelecta - Sistema Escolar SaaS

**Intelecta** é uma API abrangente para um sistema de gerenciamento escolar, desenvolvida em FastAPI. Este projeto oferece uma solução completa para administrar escolas, incluindo funcionalidades de autenticação, gerenciamento de usuários (alunos, professores, administradores), turmas, notas, frequência e muito mais.

O sistema foi projetado para ser uma plataforma SaaS (Software as a Service) flexível, capaz de atender a múltiplas escolas com isolamento de dados, garantindo que cada instituição tenha acesso apenas às suas próprias informações.

## Visão Geral

A API é estruturada em torno dos seguintes módulos principais:

- **Autenticação:** Gerencia o acesso seguro à API usando tokens JWT, com rotas para login e recuperação de informações do usuário.
- **Usuários:** Administra os dados de todos os usuários do sistema, como alunos, professores e administradores.
- **Alunos e Professores:** Módulos específicos para gerenciar informações detalhadas de alunos e professores.
- **Matrículas e Turmas:** Permite matricular alunos em turmas e gerenciar as próprias turmas.
- **Conteúdos e Atividades:** Oferece funcionalidades para criar e gerenciar unidades curriculares, conteúdos e atividades de aula.
- **Notas e Frequência:** Ferramentas para registrar o desempenho acadêmico e a frequência dos alunos.
- **Dashboard e Relatórios:** Fornece dados agregados e relatórios para uma visão geral do sistema.

## Tecnologias Utilizadas

- **FastAPI:** Framework web moderno e de alta performance para a construção da API.
- **SQLAlchemy:** ORM para interação com o banco de dados SQL.
- **Pydantic:** Utilizado para validação e serialização de dados.
- **Uvicorn:** Servidor ASGI para rodar a aplicação.
- **SQLite:** Banco de dados leve e baseado em arquivos, ideal para desenvolvimento e prototipagem.
- **Nix:** Gerenciador de pacotes que garante um ambiente de desenvolvimento reprodutível e isolado.

## Configuração do Ambiente

O ambiente de desenvolvimento é configurado através do arquivo `.idx/dev.nix`, que garante a consistência das dependências e ferramentas.

O arquivo `dev.nix` instala o **Python 3.11**, o **SQLite** e as bibliotecas Python necessárias, como `FastAPI`, `SQLAlchemy`, `Uvicorn` e `Pytest`. Além disso, configura extensões do VS Code para facilitar o desenvolvimento, como o suporte a Python e o cliente de banco de dados SQLite.

As dependências Python estão listadas em `requirements.txt`.

## Como Executar a Aplicação

1. **Instale as dependências (automático no ambiente Nix):**
   O ambiente Nix se encarrega de instalar todas as dependências do sistema e do Python na inicialização do workspace.

2. **Inicie o servidor:**
   O servidor Uvicorn é iniciado automaticamente ao abrir o projeto no ambiente de desenvolvimento configurado.

3. **Acesse a API e a Interface:**

   - **API:** A documentação interativa da API (Swagger) pode ser acessada em `/docs` na URL da aplicação.

   - **Interface do Usuário:** O frontend da aplicação pode ser acessado através da rota `/front/index.html`.

     Por exemplo, se a aplicação estiver rodando em `http://localhost:8000`, a interface estará em `http://localhost:8000/front/index.html`.


## Estrutura do Projeto

```
.
├── .idx/
│   ├── dev.nix           # Configuração do ambiente de desenvolvimento Nix
│   └── ...
├── front/                # Arquivos estáticos do frontend
├── routers/              # Módulos com as rotas da API
├── tests/                # Testes automatizados
├── utils/                # Funções utilitárias (segurança, etc.)
├── main.py               # Ponto de entrada da aplicação FastAPI
├── models.py             # Modelos de dados do SQLAlchemy
├── schemas.py            # Esquemas de dados do Pydantic
├── database.py           # Configuração do banco de dados
├── requirements.txt      # Dependências Python
└── README.md             # Este arquivo
```

## Testes Automatizados

O projeto inclui uma suíte de testes automatizados usando **Pytest** para garantir a qualidade e a estabilidade do código. A cobertura de testes é monitorada para manter um alto padrão de confiabilidade.

Para rodar os testes, execute o script:
```bash
./RUN_TESTS.sh
```

## Contribuidores

- Amanda Fonseca Joaquim - RA: 42321095 - [GitHub](https://github.com/mandybang)
- Felipe Bastos - RA: 42321681 - [GitHub](https://github.com/FelipeBastos2)
- Gabriella Oliveira Nogueira - RA: 42321688 - [GitHub](https://github.com/GabriellaNogueira1)
- Guilherme Arrais - RA: 42413847 - [GitHub](https://github.com/GuiArrais)
- Neisson Junio - RA: 42420479 - [GitHub](https://github.com/Neissonjr)
- Ana Luiza Gonçalves - RA: 42523109 - [GitHub](https://github.com/Morenaana)
- Yann Reis - RA: 42414810 - [GitHub](https://github.com/YannReis)
