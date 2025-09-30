from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.security import get_password_hash

router = APIRouter()

# Listar usuários
@router.get("/", response_model = list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

#Criar usuários 
@router.post("/", response_model = schemas.UserOut) 
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o email já foi usado
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail = "Este email já foi cadastrado")

    hashed_pw = get_password_hash(user.password)
    new_user = models.User(
        name = user.name,
        email = user.email,
        hashed_password = hashed_pw,
        role = user.role,
        school_id = 1 #settado como 1 somente pra testes, quando tiver com mais de uma opção de escola é só mudar pro school id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{user_id}",response_model = schemas.UserOut)
def update_user(
    user_id: int = Path(..., description = "ID do usuário que será atualizado"),
    user_data: schemas.UserCreate = Depends(),
    db: Session = Depends(get_db)
    ):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    # checa se o usuário está no db
    if not db_user:
        raise HTTPException(status_code = 404, detail="Usuário não encontrado") 
    
    # atualização dos dados (não altera a senha)
    db_user.name = user_data.name
    db_user.email = user_data.email
    db_user.role = user_data.role

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code = 404, detail = "usuário não encontrado")

    db.delete(db_user)
    db.commit()
    return {"detail": "Usuário excluído."}