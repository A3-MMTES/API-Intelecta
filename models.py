from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum

# Roles
class RoleEnum(str, enum.Enum):
    admin = "admin"
    student = "student"
    teacher = "teacher"

# School
class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="school", cascade="all, delete-orphan")

# User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.student)
    is_active = Column(Boolean, default=True)

    school = relationship("School", back_populates="users")