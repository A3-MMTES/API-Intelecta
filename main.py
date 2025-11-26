from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import auth, users, students, teachers, classes, grades, attendance, reports, settings, enrollments, units, activities, dashboard, questions, contents
from database import Base, engine, get_db
import models
from sqlalchemy.orm import Session
from utils.security import get_password_hash

# Cria o banco de dados e as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intelecta - Sistema Escolar SaaS",
    version="0.0.1",
    description="API do sistema escolar Intelecta"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (POST, GET, etc)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Monta a pasta "front" como um diretório estático
app.mount("/front", StaticFiles(directory="front"), name="front")


# Cria um backdoor de admin quando inicia
@app.on_event("startup")
def startup_event():
    db: Session = next(get_db())

    # Garante que a escola padrão exista
    default_school = db.query(models.School).filter(models.School.id == 1).first()
    if not default_school:
        default_school = models.School(id=1, name="Escola Padrão")
        db.add(default_school)
        db.commit()
        db.refresh(default_school)

    # Garante que o usuário admin exista
    admin_user = db.query(models.User).filter(models.User.email == "admin@intelecta.com").first()
    if not admin_user:
        hashed_password = get_password_hash("admin123")
        new_admin = models.User(
            name="Admin",
            email="admin@intelecta.com",
            hashed_password=hashed_password,
            role=models.RoleEnum.admin,
            school_id=default_school.id,
            is_active=True
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

# Registro de rotas
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/users", tags=["Usuários"])
app.include_router(students.router, prefix="/students", tags=["Alunos"])
app.include_router(teachers.router, prefix="/teachers", tags=["Professores"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Matrículas"])
app.include_router(classes.router, prefix="/classes", tags=["Turmas"])
app.include_router(grades.router, prefix="/grades", tags=["Notas"])
app.include_router(attendance.router, prefix="/attendance", tags=["Presença"])
app.include_router(reports.router, prefix="/reports", tags=["Relatórios"])
app.include_router(units.router, prefix="/units", tags=["Unidades Curriculares"]) # Tag atualizada
app.include_router(activities.router, prefix="/activities", tags=["Atividades"])
app.include_router(questions.router, prefix="/questions", tags=["Questões"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(contents.router, prefix="/contents", tags=["Conteúdos"])

# app.include_router(settings.router, prefix="/settings", tags=["Settings"])

# Rotas de verificação / status
@app.get("/")
def root():
    return {"message" : "A API está online (e aparentemente funcionando)"}

@app.get("/ping")
def ping():
    return {"msg": "pong"}
