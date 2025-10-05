from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from utils.roles import require_role

router = APIRouter()

# criar aluno (admin)
@router.post("/", response_model = schemas.StudentOut)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    db_student = db.query(models.Student).filter(
        models.Student.registration_number == student.registration_number
    ).first()
    if db_student:
        raise HTTPException(status_code = 400, detail = "Matrícula já cadastrada")

    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# listar alunos (admin)
@router.get("/", response_model = list[schemas.StudentOut])
def list_students(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(require_role(["admin"]))
):
    return db.query(models.Student).all()

# bucar por id (admin ou aluno)
@router.get("/{student_id}", response_model = schemas.StudentOut)
def get_student(   
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "student"]))
    ):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code = 404, detail = "Aluno não encontrado")

    # se o user não for admin, só poderá ver o próprio perfil 
    if current_user.role != "admin" and current_user.id != student.user_id:
        raise HTTPException(status_code = 403, detail = "Acesso negado")

    return student

# Atualizar aluno (admin)
@router.put("/{student_id}", response_model = schemas.StudentOut)
def update_student(
    student_id: int,
    update_data: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code = 404, detail = "Aluno não encontrado")

    for key, value in update_data.dict(exclude_unset = True).items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student

# Deletar (admin)
@router.delete("/{student_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_student(
     student_id: int,
     db: Session = Depends(get_db),
     current_user: models.User = Depends(require_role(["admin"]))
):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        return HTTPexception(status_code = 404, detail = "Aluno não encontrado")

    db.delete(student)
    db.commit()
    return None