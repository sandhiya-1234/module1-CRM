from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.repos.inventory_repo import InventoryRepo
from app.services.inventory_service import InventoryService
from app.schemas import ProductCreate, ProductOut
from app.database import SessionLocal

router = APIRouter(prefix="/inventory", tags=["inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    svc = InventoryService(db, InventoryRepo)
    return svc.create_product(payload.name, payload.sku, payload.opening_stock)

@router.post("/{pid}/reserve")
def reserve_stock(pid: int, qty: int, db: Session = Depends(get_db)):
    svc = InventoryService(db, InventoryRepo)
    try:
        product = svc.reserve_stock(pid, qty)
        return {"product_id": product.id, "new_stock": product.stock}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
