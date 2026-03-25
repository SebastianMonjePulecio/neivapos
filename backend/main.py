from fastapi import FastAPI
from backend.database import engine, Base

from backend.routes import products, sales, auth

# Crear app
app = FastAPI()

# Crear tablas
Base.metadata.create_all(bind=engine)

# Registrar rutas
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(auth.router)