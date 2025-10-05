from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

# Roles
class RoleEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

# User base
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum

# User create
class UserCreate(UserBase):
    password: str

# User output
class UserOut(UserBase):
    id: int
    school_id: Optional[int] = None
    is_active: bool

    class Config:
        orm_mode = True

# User update
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    password: Optional[str] = None

# Student base
class StudentBase(BaseModel):
    registration_number: str
    course: Optional[str] = None

# Student create
class StudentCreate(StudentBase):
    user_id: int

# Student update
class StudentUpdate(BaseModel):
    registration_number: Optional[str] = None
    course: Optional[str] = None

# Student output
class StudentOut(StudentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True