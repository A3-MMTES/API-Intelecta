from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.security import get_current_user
from utils.roles import require_role

router = APIRouter()

# Listar professores (admin)
@router.get("/", response_model=list[schemas.TeacherOut])
def list_teachers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    return db.query(models.Teacher).all()

# Criar professor (admin)
@router.post("/", response_model=schemas.TeacherOut)
def create_teacher(
    teacher: schemas.TeacherCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == teacher.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

# Buscar professor por ID (admin ou próprio professor)
@router.get("/{teacher_id}", response_model=schemas.TeacherOut)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    if current_user.role != "admin" and current_user.id != teacher.user_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return teacher

# Atualizar professor (admin)
@router.put("/{teacher_id}", response_model=schemas.TeacherOut)
def update_teacher(
    teacher_id: int,
    update_data: schemas.TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher

# Deletar professor (admin)
@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    db.delete(teacher)
    db.commit()
    return {"detail": "Professor excluído."}
