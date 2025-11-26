
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.security import get_current_user
from utils.roles import require_role
from typing import List

router = APIRouter()

# Dependência para garantir que o usuário é admin ou professor
is_admin_or_teacher = require_role(["admin", "teacher"])

# Criar uma nova nota (apenas para admin ou professor)
@router.post("/", response_model=schemas.GradeOut, dependencies=[Depends(is_admin_or_teacher)])
def create_grade(grade_data: schemas.GradeCreate, db: Session = Depends(get_db)):
    # Verifica se a atividade e o aluno existem
    activity = db.query(models.Activity).filter(models.Activity.id == grade_data.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    student = db.query(models.User).filter(models.User.id == grade_data.student_id, models.User.role == 'student').first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    new_grade = models.Grade(**grade_data.model_dump())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

# Listar todas as notas (acessível para admin e professores)
@router.get("/", response_model=List[schemas.GradeOut], dependencies=[Depends(is_admin_or_teacher)])
def list_grades(db: Session = Depends(get_db)):
    return db.query(models.Grade).all()

# Buscar notas por atividade específica
@router.get("/activity/{activity_id}", response_model=List[schemas.GradeOut])
def get_grades_by_activity(activity_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    grades = db.query(models.Grade).filter(models.Grade.activity_id == activity_id).all()
    if not grades:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para esta atividade")
    return grades

# Buscar notas de um aluno específico
@router.get("/student/{student_id}", response_model=List[schemas.GradeOut])
def get_grades_by_student(student_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Adicionar lógica de permissão se necessário (ex: um aluno só pode ver suas próprias notas)
    return db.query(models.Grade).filter(models.Grade.student_id == student_id).all()

# Atualizar uma nota (apenas para admin ou professor)
@router.put("/{grade_id}", response_model=schemas.GradeOut, dependencies=[Depends(is_admin_or_teacher)])
def update_grade(grade_id: int, grade_data: schemas.GradeUpdate, db: Session = Depends(get_db)):
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    
    update_data = grade_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(grade, key, value)
    
    db.commit()
    db.refresh(grade)
    return grade

# Deletar uma nota (apenas para admin ou professor)
@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin_or_teacher)])
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    
    db.delete(grade)
    db.commit()
    return

