from app.schemas import ProductCreate, ProductUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from app import models
from app.exceptions import DuplicateSKUError, ProductNotFoundError
import logging

logger = logging.getLogger(__name__)


def create_product(product: ProductCreate, db: Session):
    db_product = models.ProductDB(**product.model_dump())
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
        logger.info("Created product", extra={"sku": product.sku})
    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate SKU attempted", extra = {"sku": product.sku})
        raise DuplicateSKUError("SKU already exists")
    return db_product

def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None, 
        ):
    stmt = select(models.ProductDB)
    if category:
        stmt = stmt.where(models.ProductDB.category == category)
    stmt = stmt.offset(skip).limit(limit)
    result = db.execute(stmt)
    return result.scalars().all()

def update_product(
        product_id: int,
        product: ProductCreate,
        db: Session 
):
    db_product = db.get(models.ProductDB, product_id)

    if not db_product:
        raise ProductNotFoundError("Product not found")
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

def patch_product(
        product_id: int,
        product_update: ProductUpdate,
        db: Session
):
    db_product = db.get(models.ProductDB, product_id)

    if not db_product:
        raise ProductNotFoundError("Product not found")
    
    update_data = product_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(product_id: int, db: Session):
    db_product = db.get(models.ProductDB, product_id)
    if not db_product:
        raise ProductNotFoundError("Product not found")
    
    db.delete(db_product)
    db.commit()

    return db_product 