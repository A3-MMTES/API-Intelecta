from fastapi import FastAPI
from routers import auth, users, students, teachers, classes, grades, attendance, reports, settings
from database import Base, engine
import models 

# Cria o banco de dados e as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Intelecta", version = "0.0.1")

# inclusão das rotas
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(students.router, prefix="/students", tags=["Students"])
# app.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])
# app.include_router(classes.router, prefix="/classes", tags=["Classes"])
# app.include_router(grades.router, prefix="/grades", tags=["Grades"])
# app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
# app.include_router(reports.router, prefix="/reports", tags=["Reports"])
# app.include_router(settings.router, prefix="/settings", tags=["Settings"])

@app.get("/")
def root():
    return {"message" : "A API está online (e aparentemente funcionando)"} 

@app.get("/ping")
def ping():
    return {"msg": "pong"}

    