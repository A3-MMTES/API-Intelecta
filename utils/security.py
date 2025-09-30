from passlib.context import CryptContext 

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_password_hash(password: str) -> str: # gera a variável password e já atribui que ela é uma string, e depois denota que a saída será uma string em hash
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: # compara as duas senhas para ver se é válida (padrão e hash), se coincidirem retorna True (senha correta)
    return pwd_context.verify(plain_password, hashed-password) 