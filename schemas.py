from pydantic import BaseModel, ConfigDict
from models import RoleEnum, ContentTypeEnum
from typing import Optional, List
from datetime import date

# ======================================================
# Módulo de Conteúdo (ContentModule)
# ======================================================

class ContentModuleBase(BaseModel):
    type: ContentTypeEnum
    content: str

class ContentModuleCreate(ContentModuleBase):
    unit_id: int
    order: Optional[int] = 0

class ContentModuleUpdate(BaseModel):
    type: Optional[ContentTypeEnum] = None
    content: Optional[str] = None
    order: Optional[int] = None

class ContentModule(ContentModuleBase):
    id: int
    unit_id: int
    order: int
    model_config = ConfigDict(from_attributes=True)

# ======================================================
# Respostas (Answers)
# ======================================================
class AnswerBase(BaseModel):
    question_id: int
    option_id: int

class AnswerCreate(BaseModel):
    option_id: int

class Answer(AnswerBase):
    id: int
    student_id: int
    model_config = ConfigDict(from_attributes=True)

# ======================================================
# Opções (para Questões)
# ======================================================

class OptionBase(BaseModel):
    text: str
    is_correct: bool

class OptionCreate(OptionBase):
    pass

class OptionUpdate(BaseModel):
    text: Optional[str] = None
    is_correct: Optional[bool] = None

class Option(OptionBase):
    id: int
    question_id: int
    model_config = ConfigDict(from_attributes=True)

# ======================================================
# Questão
# ======================================================

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    options: List[OptionCreate]

class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    options: Optional[List[OptionUpdate]] = None

class Question(QuestionBase):
    id: int
    activity_id: int
    options: List[Option] = []
    answers: List[Answer] = []
    model_config = ConfigDict(from_attributes=True)


# ======================================================
# Atividade
# ======================================================

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    unit_id: int

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    unit_id: Optional[int] = None

class Activity(ActivityBase):
    id: int
    questions: List[Question] = []
    model_config = ConfigDict(from_attributes=True)


# ======================================================
# Unidade (Unit)
# ======================================================

class UnitBase(BaseModel):
    name: str
    description: Optional[str] = None
    imageUrl: Optional[str] = None

class UnitCreate(UnitBase):
    pass

class UnitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    imageUrl: Optional[str] = None

class Unit(UnitBase):
    id: int
    content_modules: List[ContentModule] = []
    model_config = ConfigDict(from_attributes=True)

# ======================================================
# Usuário
# ======================================================

class UserBase(BaseModel):
    name: str
    email: str
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    school_id: int
    model_config = ConfigDict(from_attributes=True)


# ======================================================
# Aluno
# ======================================================

class StudentBase(BaseModel):
    registration_number: str
    course: Optional[str] = None

class StudentCreate(StudentBase):
    user_id: int

class StudentUpdate(BaseModel):
    registration_number: Optional[str] = None
    course: Optional[str] = None

class StudentOut(StudentBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


# ======================================================
# Professor
# ======================================================

class TeacherBase(BaseModel):
    subject: Optional[str] = None
    hire_date: Optional[date] = None

class TeacherCreate(TeacherBase):
    user_id: int

class TeacherUpdate(BaseModel):
    subject: Optional[str] = None
    hire_date: Optional[date] = None

class TeacherOut(TeacherBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


# ======================================================
# Turma
# ======================================================

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
    model_config = ConfigDict(from_attributes=True)


# ======================================================
# Matrícula (Enrollment)
# ======================================================

class EnrollmentBase(BaseModel):
    class_id: int
    student_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(EnrollmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ======================================================
# Notas
# ======================================================

class GradeBase(BaseModel):
    grade_value: float

class GradeCreate(GradeBase):
    student_id: int
    activity_id: int # Corrigido: de class_id para activity_id

class GradeUpdate(BaseModel):
    grade_value: Optional[float] = None

class GradeOut(GradeBase):
    id: int
    student_id: int
    activity_id: int # Corrigido: de class_id para activity_id
    model_config = ConfigDict(from_attributes=True)


# ======================================================
# Presenças
# ======================================================

class AttendanceBase(BaseModel):
    date: date
    status: str

class AttendanceCreate(AttendanceBase):
    student_id: int
    class_id: int

class AttendanceUpdate(BaseModel):
    status: Optional[str] = None

class AttendanceOut(AttendanceBase):
    id: int
    student_id: int
    class_id: int
    model_config = ConfigDict(from_attributes=True)

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    unit_id: int


class ActivityCreate(ActivityBase):
    questions: Optional[List[QuestionCreate]] = None   # AQUI!


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    unit_id: Optional[int] = None
    questions: Optional[List[QuestionCreate]] = None   # E AQUI!


class Activity(ActivityBase):
    id: int
    questions: List[Question] = []
    model_config = ConfigDict(from_attributes=True)