
from fastapi import FastAPI
from routers import auth, users, students, teachers, classes, grades, attendance, reports, settings, enrollments
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

# Cria um backdoor de admin quando inicia 
@app.on_event("startup")
def startup_event():
    db: Session = next(get_db())
    admin_user = db.query(models.User).filter(models.User.email == "admin@intelecta.com").first()
    if not admin_user:
        hashed_password = get_password_hash("admin123")
        new_admin = models.User(
            name="Admin",
            email="admin@intelecta.com",
            hashed_password=hashed_password,
            role=models.RoleEnum.admin,
            school_id=1, 
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
# app.include_router(settings.router, prefix="/settings", tags=["Settings"])

# Rotas de verificação / status
@app.get("/")
def root():
    return {"message" : "A API está online (e aparentemente funcionando)"} 

@app.get("/ping")
def ping():
    return {"msg": "pong"}

    