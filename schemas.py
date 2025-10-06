from pydantic import BaseModel
from models import RoleEnum
from typing import Optional

# Usuário 

class UserBase(BaseModel):
    name: str
    email: str
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: RoleEnum | None = None

class UserOut(UserBase):
    id: int
    is_active: bool
    school_id: int

    class Config:
        orm_mode = True

# Aluno

class StudentBase(BaseModel):
    registration_number: str
    course: str | None = None

class StudentCreate(StudentBase):
    user_id: int

class StudentUpdate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Professor
class TeacherBase(BaseModel):
    subject: Optional[str] = None
    hire_date: Optional[str] = None

# Teacher create
class TeacherCreate(TeacherBase):
    user_id: int

# Teacher update
class TeacherUpdate(BaseModel):
    subject: Optional[str] = None
    hire_date: Optional[str] = None

# Teacher output
class TeacherOut(TeacherBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True