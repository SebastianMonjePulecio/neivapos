from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import schemas, models
from backend.database import get_db
from backend.security import (
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()

# 🔐 REGISTER
@router.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    ...

# 🔑 LOGIN
@router.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}

# 🛡️ RUTA PROTEGIDA
@router.get("/usuarios")
def get_usuarios(user: str = Depends(get_current_user)):
    return {"mensaje": f"Hola {user}"}