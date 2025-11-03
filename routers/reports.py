from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
from utils.roles import require_role

router = APIRouter()

# Relatório de desempenho por aluno
@router.get("/student/{student_id}")
def get_student_report(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    student = db.query(models.User).filter(models.User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    avg_grade = db.query(func.avg(models.Grade.grade_value)).filter(models.Grade.student_id == student_id).scalar()
    avg_grade = round(avg_grade, 2) if avg_grade else None

    total_classes = db.query(models.Attendance).filter(models.Attendance.student_id == student_id).count()
    presents = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id,
        models.Attendance.status == "present"
    ).count()
    attendance_rate = round((presents / total_classes) * 100, 2) if total_classes > 0 else None

    return {
        "student_id": student.id,
        "student_name": student.name,
        "average_grade": avg_grade,
        "attendance_rate": attendance_rate
    }


# Relatório geral da turma
@router.get("/class/{class_id}")
def get_class_report(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "teacher"]))
):
    class_ = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    avg_class_grade = (
        db.query(func.avg(models.Grade.grade_value))
        .filter(models.Grade.class_id == class_id)
        .scalar()
    )
    avg_class_grade = round(avg_class_grade, 2) if avg_class_grade else None

    total_att = db.query(models.Attendance).filter(models.Attendance.class_id == class_id).count()
    presents = db.query(models.Attendance).filter(
        models.Attendance.class_id == class_id,
        models.Attendance.status == "present"
    ).count()
    attendance_rate = round((presents / total_att) * 100, 2) if total_att > 0 else None

    return {
        "class_id": class_.id,
        "class_name": class_.name,
        "average_grade": avg_class_grade,
        "attendance_rate": attendance_rate
    }
