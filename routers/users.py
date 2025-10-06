from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.security import get_password_hash, get_current_user
from utils.roles import require_role 

router = APIRouter()

# Listar usuários (admin)
@router.get("/", response_model=list[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    return db.query(models.User).all()

# Criar usuários (admin)
@router.post("/", response_model=schemas.UserOut) 
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    hashed_password = get_password_hash(user.password)
    # school_id está fixo em 1
    new_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password, role=user.role, school_id=1)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Deletar usuário (admin)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(user)
    db.commit()
    return None

# Ver qual usuário estou logado (geral)
@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Buscar por ID (admin)
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# Atualizar usuário (admin ou o próprio)
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    update_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != models.RoleEnum.admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # for key, value in update_data.dict(exclude_unset=True).items():
    update_dict = update_data.dict(exclude_unset=True)

    if "password" in update_dict and update_dict["password"]:
        user.hashed_password = get_password_hash(update_dict["password"])
        del update_dict["password"]
    
    for key, value in update_dict.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
