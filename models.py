from sqlalchemy import *
from sqlalchemy.orm import relationship
from database import Base
import enum

# Enum serve pra travar as opções de cargos (roles), então não vai divergir dos 3 possíveis 
class RoleEnum(str, enum.Enum):
    admin = "admin"
    student = "student"
    teacher = "teacher"

class School(Base):
    __tablename__ = "schools" 

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    users = relationship("User", back_populates = "school")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable = False)

    name = Column(String, nullable = False)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password = Column(String, nullable = False)

    role = Column(Enum(RoleEnum), nullable = False, default = RoleEnum.student)
    is_active = Column(Boolean, default = True)

    school = relationship("School", back_populates = "users")
    student = relationship("Student", back_populates="user", uselist=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), unique = True)
    registration_number = Column(String, unique = True, index = True)
    course = Column(String, nullable = True)

    user = relationship("User", back_populates = "student")

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), unique = True)
    subject = Column(String, nullable = False)
    hire_date = Column(String, nullable = False)

    user = relationship("User")