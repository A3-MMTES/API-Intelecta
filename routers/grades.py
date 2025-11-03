from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.security import get_current_user
from utils.roles import require_role

router = APIRouter()

# Criar nota (admin ou professor)
@router.post("/", response_model=schemas.GradeOut)
def create_grade(
    grade_data: schemas.GradeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    new_grade = models.Grade(**grade_data.dict())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

# Listar todas as notas (admin e professor)
@router.get("/", response_model=list[schemas.GradeOut])
def list_grades(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    return db.query(models.Grade).all()

# Buscar notas por aluno
@router.get("/student/{student_id}", response_model=list[schemas.GradeOut])
def get_grades_by_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher", "student"]))
):
    return db.query(models.Grade).filter(models.Grade.student_id == student_id).all()

# Buscar notas por turma
@router.get("/class/{class_id}", response_model=list[schemas.GradeOut])
def get_grades_by_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    return db.query(models.Grade).filter(models.Grade.class_id == class_id).all()

# Atualizar nota (admin ou professor)
@router.put("/{grade_id}", response_model=schemas.GradeOut)
def update_grade(
    grade_id: int,
    grade_data: schemas.GradeUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Nota não encontrada")

    for key, value in grade_data.dict(exclude_unset=True).items():
        setattr(grade, key, value)

    db.commit()
    db.refresh(grade)
    return grade

# Deletar nota (admin ou professor)
@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Nota não encontrada")

    db.delete(grade)
    db.commit()
    return {"detail": "Nota removida com sucesso."}