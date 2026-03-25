from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.product import ProductCreate
from backend.models.product import Product
from backend.database import get_db

router = APIRouter()

@router.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/products/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()