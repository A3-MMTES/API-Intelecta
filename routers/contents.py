from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from auth_utils import get_current_user

router = APIRouter(
    prefix="/contents",
    tags=["contents"],
)

# Proteger todas as rotas de conteúdo
def get_current_teacher_or_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role not in [models.RoleEnum.teacher, models.RoleEnum.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a professores e administradores",
        )
    return current_user

@router.post("/", response_model=schemas.ContentModule, status_code=status.HTTP_201_CREATED)
def create_content_module(
    module: schemas.ContentModuleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_teacher_or_admin),
):
    """
    Cria um novo módulo de conteúdo para uma unidade curricular.
    - **type**: Tipo do conteúdo (`TEXT`, `IMAGE`, `LINK`).
    - **content**: O conteúdo em si (texto ou URL).
    - **unit_id**: ID da unidade à qual o módulo pertence.
    - **order**: Posição do módulo na sequência.
    """
    db_unit = db.query(models.Unit).filter(models.Unit.id == module.unit_id).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    db_module = models.ContentModule(**module.model_dump())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

@router.get("/by_unit/{unit_id}", response_model=List[schemas.ContentModule])
def get_content_modules_for_unit(
    unit_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Qualquer usuário logado pode ver
):
    """Obtém todos os módulos de conteúdo para uma unidade específica, ordenados."""
    modules = (
        db.query(models.ContentModule)
        .filter(models.ContentModule.unit_id == unit_id)
        .order_by(models.ContentModule.order)
        .all()
    )
    return modules

@router.put("/{module_id}", response_model=schemas.ContentModule)
def update_content_module(
    module_id: int,
    module_update: schemas.ContentModuleUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_teacher_or_admin),
):
    """
    Atualiza um módulo de conteúdo existente (conteúdo, tipo ou ordem).
    """
    db_module = db.query(models.ContentModule).filter(models.ContentModule.id == module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Módulo de conteúdo não encontrado")

    update_data = module_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_module, key, value)
    
    db.commit()
    db.refresh(db_module)
    return db_module

@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_teacher_or_admin),
):
    """Exclui um módulo de conteúdo."""
    db_module = db.query(models.ContentModule).filter(models.ContentModule.id == module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Módulo de conteúdo não encontrado")
    
    db.delete(db_module)
    db.commit()
    return
