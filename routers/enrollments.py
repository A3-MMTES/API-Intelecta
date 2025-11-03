from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.security import get_current_user
from utils.roles import require_role

router = APIRouter()

# Listar matrículas 
@router.get("/", response_model = list[schemas.EnrollmentOut])
def list_enrollments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin","teacher"]))
):
    return db.query(models.ClassStudent).all()

# Criar matrícula 
@router.post("/", response_model = schemas.EnrollmentOut)
def create_enrollment(
    enrollment: schemas.EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):

    # check se o aluno e turma existem
    class_ = db.query(models.Class).filter(models.Class.id == enrollment.class_id).first()
    student = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()

    if not class_:
        raise HTTPException(status_code = 404, detail = "Turma não encontrada")
    if not student:
        raise HTTPException(status_code = 404, detail = "Aluno não encontrado")

    # check se a matrícula existe
    existing = db.query(models.ClassStudent).filter(
        models.ClassStudent.class_id == enrollment.class_id,
        models.ClassStudent.student_id == enrollment.student_id
    ).first()

    if existing:
        raise HTTPException(status_code = 404, detail = "Aluno já matriculado nesta turma")

    new_enrollment = models.ClassStudent(**enrollment.dict())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

# Deletar matrícula
@router.delete("/{enrollment_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    enrollment = db.query(models.ClassStudent).filter(models.ClassStudent.id == enrollmen_id).first()
    if not enrollment:
        raise HTTPException(status_code = 404, detail = "Matrícula não encontrada")

    db.delete(enrollment)
    db.commit
    return {"detail": "Matrícula excluída com sucesso"}