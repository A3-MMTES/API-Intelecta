# Intelecta 

Sistema de gestão escolar voltado para instituições de ensino EAD.
---

##  Funcionalidades

- **Listar turmas**
- **Criar turmas**
- **Visualizar turma por ID**
- **Atualizar turma**
- **Excluir turma**

### Regras de acesso
| Função (role) | Permissões |
|----------------|-------------|
| `admin` | Criar, listar, visualizar, atualizar e excluir turmas |
| `teacher` | Listar e visualizar turmas |
| `student` | Sem acesso direto |

---

##  Estrutura de arquivos

```
project/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
│
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── students.py
│   ├── teachers.py
│   ├── classes.py   
│
└── utils/
    ├── security.py
    └── roles.py
```

---

##  Modelos de Dados

### models.py
```python
class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)
    schedule = Column(String, nullable=True)

    school = relationship("School")
    teacher = relationship("Teacher")
```
---

## Schemas

### schemas.py
```python
class ClassBase(BaseModel):
    name: str
    schedule: Optional[str] = None

class ClassCreate(ClassBase):
    school_id: int
    teacher_id: Optional[int] = None

class ClassUpdate(BaseModel):
    name: Optional[str] = None
    schedule: Optional[str] = None
    teacher_id: Optional[int] = None

class ClassOut(ClassBase):
    id: int
    school_id: int
    teacher_id: Optional[int] = None

    class Config:
        orm_mode = True
```
---

## Rotas (API)

### routers/classes.py
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils.security import get_current_user
from utils.roles import required_role

router = APIRouter()

@router.get("/", response_model=list[schemas.ClassOut])
def list_classes(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return db.query(models.Class).all()

@router.post("/", response_model=schemas.ClassOut)
def create_class(new_class: schemas.ClassCreate, db: Session = Depends(get_db), current_user: models.User = Depends(required_role(["admin"]))):
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
def update_class(class_id: int, update_data: schemas.ClassUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(required_role(["admin"]))):
    turma = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(turma, key, value)
    db.commit()
    db.refresh(turma)
    return turma

@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(class_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(required_role(["admin"]))):
    turma = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    db.delete(turma)
    db.commit()
    return {"detail": "Turma excluída."}
```

---

## 🔗 Integração no `main.py`

```python
app.include_router(classes.router, prefix="/classes", tags=["Classes"])
```

---

##  Testando no Swagger UI

1. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```
2. Acesse:  
    `http://localhost:8000/docs`
3. Clique em **Authorize** e insira o token JWT (via `/auth/login`).
4. Teste os endpoints:
   - `POST /classes`
   - `GET /classes`
   - `GET /classes/{id}`
   - `PUT /classes/{id}`
   - `DELETE /classes/{id}`

---

## Próximos passos

Criar o relacionamento **Aluno <-> Turma (N:N)** para permitir **matrículas e listagem de alunos por turma**.

---

**Status atual:**  
✅ CRUD de usuários  
✅ CRUD de alunos  
✅ CRUD de turmas  
Matrículas (Students ↔ Classes)
