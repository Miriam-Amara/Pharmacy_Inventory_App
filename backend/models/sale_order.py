#!/usr/bin/env python3

"""
Purchase order model.
"""

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey, String, Enum
import enum

from models.basemodel import Base, BaseModel


class SaleOrderStatus(str, enum.Enum):
    """Represents the current stage of a sale order."""

    pending = "pending"
    complete = "complete"
    cancelled = "cancel"


class SaleOrder(BaseModel, Base):
    """Represents a sale order record."""

    __tablename__ = "sale_orders"

    status = mapped_column(
        Enum(SaleOrderStatus, name="sale_order_status", create_type=True),
        default="pending"
    )
    employee_id = mapped_column(
        String(36),
        ForeignKey("employees.id", ondelete="SET NULL")
    )

    added_by = relationship("Employee", backref="sale_orders_added")
    sales = relationship(
        "Sale", back_populates="sale_order"
    )
