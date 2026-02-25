from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint, UniqueConstraint
from datetime import datetime, timezone
from app.database import Base


class ProductDB(Base):
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint("sku", name="uq_product_sku"),
        CheckConstraint("price > 0", name="check_price_positive"),
        CheckConstraint("quantity > 0", name="check_qty_positive")
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))