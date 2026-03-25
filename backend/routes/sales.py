from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.sale import SaleCreate
from backend.models.sale import Sale
from backend.models.product import Product
from backend.database import get_db
from backend.security import get_current_user 


router = APIRouter(prefix="/sales", tags=["Sales"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == sale.product_id).first()

    if not product:
        return {"error": "Producto no encontrado"}

    if product.stock < sale.quantity:
        return {"error": "Stock insuficiente"}

    total = product.price * sale.quantity

    # Descontar stock
    product.stock -= sale.quantity

    # Crear venta
    new_sale = Sale(
        product_id=product.id,
        quantity=sale.quantity,
        total=total
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale

@router.get("/product/{product_id}")
def get_sales_by_product(product_id: int, db: Session = Depends(get_db)):
    return db.query(Sale).filter(Sale.product_id == product_id).all()

@router.post("/sales/")
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)  # 👈 PROTECCIÓN
):
    # Lógica de creación de venta (similar a la función anterior)
    # ...
    return {"message": "Venta creada exitosamente"}

@router.get("/sales/stats/")
def get_sales_stats(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    sales = db.query(Sale).all()

    total_sales = len(sales)
    total_income = 0

    for sale in sales:
        product = db.query(Product).filter(Product.id == sale.product_id).first()
        if product:
            total_income += product.price * sale.quantity

    return {
        "total_sales": total_sales,
        "total_income": total_income
    }