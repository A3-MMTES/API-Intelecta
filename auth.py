from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models, schemas
from database import get_db
from utils.security import verify_password, create_access_token, get_password_hash
from auth_utils import get_current_user

router = APIRouter()


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password) or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    
    # A escola padrão é criada no startup. Aqui, apenas verificamos se ela existe.
    default_school = db.query(models.School).filter(models.School.id == 1).first()
    if not default_school:
        # Em um ambiente de produção, seria bom logar este erro.
        raise HTTPException(status_code=500, detail="Default school not found.")

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role, 
        school_id=default_school.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
