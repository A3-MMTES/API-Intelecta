from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.roles import require_role

router = APIRouter()

# Registrar presença (professor ou admin)
@router.post("/", response_model=schemas.AttendanceOut)
def create_attendance(
    attendance_data: schemas.AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    new_attendance = models.Attendance(**attendance_data.dict())
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

# Listar presenças
@router.get("/", response_model=list[schemas.AttendanceOut])
def list_attendance(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    return db.query(models.Attendance).all()

# Presenças por aluno
@router.get("/student/{student_id}", response_model=list[schemas.AttendanceOut])
def get_attendance_by_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher", "student"]))
):
    return db.query(models.Attendance).filter(models.Attendance.student_id == student_id).all()

# Atualizar status (professor ou admin)
@router.put("/{attendance_id}", response_model=schemas.AttendanceOut)
def update_attendance(
    attendance_id: int,
    attendance_data: schemas.AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Registro de presença não encontrado")

    for key, value in attendance_data.dict(exclude_unset=True).items():
        setattr(attendance, key, value)

    db.commit()
    db.refresh(attendance)
    return attendance

# Deletar registro de presença
@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    db.delete(attendance)
    db.commit()
    return {"detail": "Registro de presença removido com sucesso."}
