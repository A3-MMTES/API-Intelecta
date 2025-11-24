from sqlalchemy import *
from sqlalchemy.orm import relationship, declarative_base
from database import Base
import enum
from datetime import date

# Enum para os cargos (roles)
class RoleEnum(str, enum.Enum):
    admin = "admin"
    student = "student"
    teacher = "teacher"

# Enum para os tipos de conteúdo
class ContentTypeEnum(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    LINK = "link"

class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    users = relationship("User", back_populates="school")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.student)
    is_active = Column(Boolean, default=True)
    school = relationship("School", back_populates="users")
    student = relationship("Student", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    registration_number = Column(String, unique=True, index=True)
    course = Column(String, nullable=True)
    user = relationship("User", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    subject = Column(String, nullable=True)
    hire_date = Column(Date, nullable=True)
    user = relationship("User")

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)
    schedule = Column(String, nullable=True)
    school = relationship("School")
    teacher = relationship("Teacher")
    enrollments = relationship("Enrollment", back_populates="class_")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"))
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    class_ = relationship("Class", back_populates="enrollments")
    student = relationship("Student")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    grade_value = Column(Float, nullable=False)
    student = relationship("User")
    activity = relationship("Activity")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False, default="present")
    student = relationship("User", foreign_keys=[student_id])
    class_ = relationship("Class")

class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    imageUrl = Column(String, nullable=True)
    activities = relationship("Activity", back_populates="unit", cascade="all, delete-orphan")
    content_modules = relationship("ContentModule", back_populates="unit", cascade="all, delete-orphan", order_by="ContentModule.order")

class ContentModule(Base):
    __tablename__ = "content_modules"
    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    type = Column(Enum(ContentTypeEnum), nullable=False)
    content = Column(Text, nullable=False)
    order = Column(Integer, nullable=False, default=0)
    unit = relationship("Unit", back_populates="content_modules")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    unit_id = Column(Integer, ForeignKey("units.id"))
    unit = relationship("Unit", back_populates="activities")
    questions = relationship("Question", back_populates="activity", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    activity = relationship("Activity", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="options")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    question = relationship("Question", back_populates="answers")
    option = relationship("Option")
    student = relationship("User")
