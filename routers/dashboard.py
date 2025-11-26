from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from typing import Dict, List

router = APIRouter()

@router.get("/stats", response_model=Dict[str, int])
def get_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas gerais para o dashboard.
    """
    num_units = db.query(models.Unit).count()
    num_activities = db.query(models.Activity).count()
    num_students = db.query(models.User).filter(models.User.role == 'student').count()
    num_teachers = db.query(models.User).filter(models.User.role == 'teacher').count()
    num_classes = db.query(models.Class).count()
    
    return {
        "units": num_units,
        "activities": num_activities,
        "students": num_students,
        "teachers": num_teachers,
        "classes": num_classes
    }

@router.get("/recent-activities", response_model=List[schemas.Activity])
def get_recent_activities(db: Session = Depends(get_db)):
    """
    Retorna as 5 atividades mais recentes.
    """
    recent_activities = db.query(models.Activity).order_by(models.Activity.id.desc()).limit(5).all()
    return recent_activities
