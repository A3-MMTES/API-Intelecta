from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.security import get_current_user
from utils.roles import require_role

router = APIRouter()

# Dependência para garantir que o usuário é admin ou professor
is_admin_or_teacher = require_role(["admin", "teacher"])

@router.post("/", response_model=schemas.Unit, dependencies=[Depends(is_admin_or_teacher)])
def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    """Cria uma nova unidade curricular (apenas para admins e professores)."""
    # Usando .model_dump() em vez do obsoleto .dict()
    db_unit = models.Unit(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

@router.get("/", response_model=list[schemas.Unit])
def read_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Lista todas as unidades curriculares (acessível para todos os usuários logados)."""
    units = db.query(models.Unit).offset(skip).limit(limit).all()
    return units

@router.get("/{unit_id}", response_model=schemas.Unit)
def read_unit(unit_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Obtém os detalhes de uma unidade curricular específica."""
    db_unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unidade curricular não encontrada")
    return db_unit

@router.put("/{unit_id}", response_model=schemas.Unit, dependencies=[Depends(is_admin_or_teacher)])
def update_unit(unit_id: int, unit: schemas.UnitUpdate, db: Session = Depends(get_db)):
    """Atualiza uma unidade curricular (apenas para admins e professores)."""
    db_unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unidade curricular não encontrada")
    
    # Usando .model_dump() com exclude_unset=True para atualizar apenas os campos enviados
    update_data = unit.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_unit, key, value)
        
    db.commit()
    db.refresh(db_unit)
    return db_unit

@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin_or_teacher)])
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    """Exclui uma unidade curricular (apenas para admins e professores)."""
    db_unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unidade curricular não encontrada")
        
    db.delete(db_unit)
    db.commit()
    return # Retorna 204 No Content
