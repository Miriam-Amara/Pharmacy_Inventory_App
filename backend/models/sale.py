#!/usr/bin/env python3

"""
Sale model.
"""

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Float, Enum
import enum

from models.basemodel import Base, BaseModel



class SalePaymentStatus(str, enum.Enum):
    """Payment state for an order item."""

    paid = "paid"
    unpaid = "unpaid"


class Sale(BaseModel, Base):
    """Represents a product sale record."""

    __tablename__ = "sales"

    sale_order_id = mapped_column(
        String(36), ForeignKey("sale_orders.id", ondelete="SET NULL")
    )
    product_id = mapped_column(
        String(36), ForeignKey("products.id", ondelete="SET NULL")
    )
    quantity = mapped_column(Integer, nullable=False)
    unit_selling_price = mapped_column(Float, nullable=False)
    total_selling_price = mapped_column(Float, nullable=False)
    payment_status = mapped_column(
        Enum(SalePaymentStatus, name="sale_payment_status", create_type=True),
        nullable=False
    )
    employee_id = mapped_column(
        String(36), ForeignKey("employees.id", ondelete="SET NULL")
    )

    sale_order = relationship("SaleOrder", back_populates="sales")
    product = relationship("Product", back_populates="sales")
    added_by = relationship("Employee", backref="sales")
