from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from typing import List
from auth_utils import get_current_user

router = APIRouter(tags=["questions"])


# ====================================================
# CREATE QUESTION WITH MULTIPLE CHOICE OPTIONS
# ====================================================
@router.post("/", response_model=schemas.Question)
def create_question_for_activity(
    activity_id: int,
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Apenas professor ou admin pode criar questões
    if current_user.role == models.RoleEnum.student:
        raise HTTPException(status_code=403, detail="Students cannot create questions")

    # Verifica se a atividade existe
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Cria a questão
    db_question = models.Question(
        text=question.text,
        activity_id=activity_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # Cria as opções da questão
    for opt in question.options:
        db_option = models.Option(
            text=opt.text,
            is_correct=opt.is_correct,
            question_id=db_question.id
        )
        db.add(db_option)

    db.commit()
    db.refresh(db_question)

    return db_question



# ====================================================
# STUDENT ANSWERS A QUESTION (MULTIPLE CHOICE)
# ====================================================
@router.post("/{question_id}/answers", response_model=schemas.Answer)
def answer_question(
    question_id: int,
    answer: schemas.AnswerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Apenas alunos podem responder
    if current_user.role != models.RoleEnum.student:
        raise HTTPException(status_code=403, detail="Only students can answer questions")

    # Verifica se a questão existe
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Verifica se a alternativa existe e pertence à questão
    db_option = db.query(models.Option).filter(models.Option.id == answer.option_id).first()
    if not db_option or db_option.question_id != question_id:
        raise HTTPException(status_code=404, detail="Option not found")

    # Verifica se já respondeu
    db_answer = db.query(models.Answer).filter(
        models.Answer.question_id == question_id,
        models.Answer.student_id == current_user.id
    ).first()

    # Atualiza resposta existente
    if db_answer:
        db_answer.option_id = answer.option_id
    else:
        db_answer = models.Answer(
            option_id=answer.option_id,
            question_id=question_id,
            student_id=current_user.id
        )
        db.add(db_answer)

    db.commit()
    db.refresh(db_answer)

    return db_answer



# ====================================================
# GET ALL QUESTIONS + OPTIONS FOR ONE ACTIVITY
# ====================================================
@router.get("/by_activity/{activity_id}", response_model=List[schemas.Question])
def get_questions_for_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verifica se a atividade existe
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Retorna perguntas com múltipla escolha
    return db_activity.questions
