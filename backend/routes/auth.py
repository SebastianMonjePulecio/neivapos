from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from backend.database import get_db
from backend import models
from backend.schemas.user import UserCreate, UserLogin

from backend.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()

# ======================
# REGISTER
# ======================

@router.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    new_user = models.User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario creado"}

# ======================
# LOGIN (IMPORTANTE PARA SWAGGER)
# ======================

@router.post("/login/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token({"sub": db_user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ======================
# PROTECTED ROUTE
# ======================

@router.get("/usuarios/")
def usuarios(username: str = Depends(get_current_user)):
    return {"message": f"Hola {username}"}