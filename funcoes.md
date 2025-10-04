main:
def root(): Mostra uma resposta na rota base da api (serve pra ver se tá funcionando ou não)

def ping(): serve como uma espécie de teste geral.
Se retorna "pong", o problema no momento pode ser nas rotas 
Se falhar, o erro é algo maior, como o app não ter subido direito ou o DB deu erro

database:
def get_db(): Dependência da FastAPI que gerencia as sessões com o banco de dados (Cria, fornece e fecha a sessão). Ela evita que conexões fiquem abertas desnecessariamente.

Security:
def create_access_token(): Gera um token de autenticação

def verify_access_token(): Verifica e valida o token criado com create_access_token()

def get_current_user(): Retorna qual usuário está logado e quais os seus dados 

def get_password_hash(): Transforma a senha em hash

def verify_password(): Compara a senha padrão e a hash e valida se então corretas

roles:
def require_role(roles: list[str]): Função que torna necesário um cargo específico para acessar certas rotas.

def role_checker(current_user: models.User = Depends(get_current_user)): Essa é uma dependência da FastAPI que verifica se o usuário tem o cargo necessário para acessar a rota.

auth:
def login(): Faz login. (verifica se os dados e token é válido)

users:

def list_users(): Lista todos os usuários (admin) 

def create_user(): cria um usuário novo (admin)

def delete_user(): deleta um usuário (admin)

def read_me(): Ver qual usuário estou logado (geral)

def get_user(): Buscar por ID (admin)

def update_user(): Atualizar usuário (admin ou o próprio)   