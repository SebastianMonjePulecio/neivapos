from fastapi import FastAPI
from backend.database import engine, Base
from backend.routes import products, sales, auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(products.router)
app.include_router(sales.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"mensaje": "API funcionando 🚀"}