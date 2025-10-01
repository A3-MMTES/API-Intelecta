from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class RoleEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    school_id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[RoleEnum] = None
# UserBase: campos comuns (nome, email, role).
# UserCreate: herda do UserBase + adiciona password (entrada de cadastro).
# UserUpdate: schema para atualização de usuários, com campos opcionais.
# UserOut: herda do UserBase + adiciona id, school_id e is_active (saída na resposta).
# orm_mode = True: diz pro Pydantic que pode converter um objeto SQLAlchemy (User) em JSON direto.
