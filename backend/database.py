import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 🔐 Cargar variables del .env (solo local)
load_dotenv()

# 📌 Obtener DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 🚨 Fallback para desarrollo local (si no existe .env)
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./neivapos.db"

# 🔥 Crear engine con soporte para PostgreSQL y SQLite
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

# 🔧 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📦 Base
Base = declarative_base()

# 🔌 Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()