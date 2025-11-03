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
    registration_number: Optional[str] = None
    course: Optional[str] = None

class StudentOut(StudentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Professor
class TeacherBase(BaseModel):
    subject: Optional[str] = None
    hire_date: Optional[str] = None

# create
class TeacherCreate(TeacherBase):
    user_id: int

# update
class TeacherUpdate(BaseModel):
    subject: Optional[str] = None
    hire_date: Optional[str] = None

# output
class TeacherOut(TeacherBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Turmas 
class ClassBase(BaseModel):
    name:  str
    schedule: Optional[str] = None

# crate
class ClassCreate(ClassBase):
    teacher_id: int
    school_id: Optional[int] = None

# update
class ClassUpdate(ClassBase):
    name: Optional[str] = None
    schedule: Optional[str] = None
    teacher_id: Optional[int] = None

# output
class ClassOut(ClassBase):
    id: int
    teacher_id: int
    school_id: Optional[int] = None 
    
    class Config:
        orm_mode = True

# turma
class ClassBase(BaseModel):
    name: str
    schedule: Optional[str] = None

class ClassCreate(ClassBase):
    school_id: int
    teacher_id: Optional[int] = None

class ClassUpdate(BaseModel):
    name: Optional[str] = None
    schedule: Optional[str] = None
    teacher_id: Optional[int] = None

class ClassOut(ClassBase):
    id: int
    school_id: int
    teacher_id: Optional[int] = None

    class Config:
        orm_mode = True


# associação aluno x turma 

class EnrollmentBase(BaseModel):
    class_id: int
    student_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(EnrollmentBase):
    id: int

    class config:
        orm_mode = True 
        
# Notas
class GradeBase(BaseModel):
    grade_value: float
    description: str | None = None

class GradeCreate(GradeBase):
    student_id: int
    class_id: int

class GradeUpdate(BaseModel):
    grade_value: float | None = None
    description: str | None = None

class GradeOut(GradeBase):
    id: int
    student_id: int
    class_id: int

    class Config:
        orm_mode = True

# Presenças
class AttendanceBase(BaseModel):
    date: str
    status: str

class AttendanceCreate(AttendanceBase):
    student_id: int
    class_id: int

class AttendanceUpdate(BaseModel):
    status: str | None = None

class AttendanceOut(AttendanceBase):
    id: int
    student_id: int
    class_id: int

    class Config:
        orm_mode = True

from datetime import date

