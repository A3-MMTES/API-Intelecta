from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from typing import List
from utils.security import get_current_user
from utils.roles import require_role

router = APIRouter()

# Dependência para garantir que o usuário é admin ou professor
is_admin_or_teacher = require_role(["admin", "teacher"])

@router.post("/", response_model=schemas.Activity, dependencies=[Depends(is_admin_or_teacher)])
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    """Cria uma nova atividade com suas questões e opções de forma atômica."""
    
    # Cria a atividade principal
    db_activity = models.Activity(
        title=activity.title,
        unit_id=activity.unit_id
    )

    # Constrói as questões e opções em memória
    for question_data in activity.questions:
        new_question = models.Question(text=question_data.text)
        for option_data in question_data.options:
            new_option = models.Option(text=option_data.text, is_correct=option_data.is_correct)
            new_question.options.append(new_option)
        db_activity.questions.append(new_question)

    # Adiciona a atividade (com suas questões e opções aninhadas) à sessão
    db.add(db_activity)
    # Comete a transação uma única vez
    db.commit()
    # Atualiza o objeto db_activity com os IDs gerados pelo banco de dados
    db.refresh(db_activity)

    return db_activity

@router.get("/", response_model=List[schemas.Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Lista todas as atividades. Acessível para todos os usuários logados."""
    activities = db.query(models.Activity).offset(skip).limit(limit).all()
    return activities

@router.get("/{activity_id}", response_model=schemas.Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Obtém os detalhes de uma atividade específica."""
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return db_activity

@router.get("/{activity_id}/grades", response_model=List[schemas.GradeOut])
def get_activity_grades(activity_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Obtém todas as notas de uma atividade específica."""
    grades = db.query(models.Grade).filter(models.Grade.activity_id == activity_id).all()
    if not grades:
        return []
    return grades

@router.put("/{activity_id}", response_model=schemas.Activity, dependencies=[Depends(is_admin_or_teacher)])
def update_activity(activity_id: int, activity: schemas.ActivityUpdate, db: Session = Depends(get_db)):
    """Atualiza uma atividade, incluindo suas questões e opções, de forma atômica."""
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    # Atualiza os campos da atividade
    update_data = activity.model_dump(exclude_unset=True)
    db_activity.title = update_data.get('title', db_activity.title)
    db_activity.unit_id = update_data.get('unit_id', db_activity.unit_id)

    # Se 'questions' estiver nos dados de atualização, substitui as questões existentes
    if 'questions' in update_data:
        new_questions = []
        for q_data in update_data['questions']:
            new_question = models.Question(text=q_data['text'])
            for o_data in q_data.get('options', []):
                new_option = models.Option(text=o_data['text'], is_correct=o_data['is_correct'])
                new_question.options.append(new_option)
            new_questions.append(new_question)
        db_activity.questions = new_questions
    
    # Comete a transação uma única vez
    db.commit()
    db.refresh(db_activity)

    return db_activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin_or_teacher)])
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """Exclui uma atividade e todos os seus componentes."""
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    db.delete(db_activity)
    db.commit()
    return
