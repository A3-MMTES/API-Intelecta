from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.security import get_current_user
from utils.roles import require_role

router = APIRouter()

@router.get("/", response_model=list[schemas.ClassOut])
def list_classes(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return db.query(models.Class).all()

@router.post("/", response_model=schemas.ClassOut)
def create_class(new_class: schemas.ClassCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["admin"]))):
    db_class = models.Class(**new_class.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

@router.get("/{class_id}", response_model=schemas.ClassOut)
def get_class(class_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    turma = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return turma

@router.put("/{class_id}", response_model=schemas.ClassOut)
def update_class(class_id: int, update_data: schemas.ClassUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["admin"]))):
    turma = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(turma, key, value)
    db.commit()
    db.refresh(turma)
    return turma

@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(class_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["admin"]))):
    turma = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    db.delete(turma)
    db.commit()
    return {"detail": "Turma excluída."}