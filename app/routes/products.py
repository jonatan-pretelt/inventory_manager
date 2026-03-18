from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Product, ProductCreate, ProductUpdate
from app.services import product_service
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    with db.begin():
        logger.info("Creating product", extra={"sku": product.sku})
        product = product_service.create_product(product, db)
        db.refresh(product)
        return product


@router.get("/", response_model=list[Product])
def list_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    logger.info("Getting products", extra=None)
    return product_service.get_products(
        db=db, skip=skip, limit=limit, category=category
    )


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int, product: ProductCreate, db: Session = Depends(get_db)
):
    product_updated = product_service.update_product(product_id, product, db)
    return product_updated


@router.patch("/{product_id}", response_model=Product)
def patch_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    updated = product_service.patch_product(product_id, product, db)
    return updated


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_deleted = product_service.delete_product(product_id, db)
    if product_deleted:
        return {"message": "Product deleted successfully"}
