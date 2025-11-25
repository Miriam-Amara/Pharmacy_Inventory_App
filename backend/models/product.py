#!/usr/bin/env python3

"""
Product model.
"""

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey, String, Float, Integer, Boolean

from models.basemodel import Base, BaseModel


class Product(BaseModel, Base):
    """Represents a product in the pharmacy."""

    __tablename__ = "products"

    barcode = mapped_column(String(20), unique=True)
    image_filepath = mapped_column(String(300), unique=True)
    name = mapped_column(String(500), nullable=False, unique=True)
    category_id = mapped_column(
        String(36),
        ForeignKey("categories.id", ondelete="SET NULL")
    )
    brand_id = mapped_column(
        String(36),
        ForeignKey("brands.id", ondelete="SET NULL")
    )
    quantity_in_stock = mapped_column(Integer, default=0)
    unit_cost_price = mapped_column(Float, default=0.00)
    unit_selling_price = mapped_column(Float, default=0.00)
    ordering_cost = mapped_column(Float, default=0.00)
    lead_time = mapped_column(Integer)
    holding_cost_rate = mapped_column(Float, default=0.20)
    average_unit_cost_90d = mapped_column(Float)
    average_ordering_cost_90d = mapped_column(Float)
    average_daily_demand_90d = mapped_column(Float)
    reordering_point = mapped_column(Integer)
    safety_stock = mapped_column(Integer)
    economic_ordering_quantity = mapped_column(Integer)
    is_below_reorder = mapped_column(Boolean)
    is_below_safety_stock = mapped_column(Boolean)
    employee_id = mapped_column(
        String(36),
        ForeignKey("employees.id", ondelete="SET NULL")
    )

    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    added_by = relationship("Employee", backref="products_added")
    sales = relationship("Sale", back_populates="product")
    purchases = relationship("Purchase", back_populates="product")
    stock_level = relationship("StockLevel", back_populates="product")

    @classmethod
    def search_product_by_barcode(cls, barcode: str):
        """Find a product using barcode"""
        from models import storage
        return storage.search_product_by_barcode(barcode)
