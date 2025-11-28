#!/usr/bin/env python3

"""
Purchase order model.
"""

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey, String, Enum, Float
import enum

from models.basemodel import Base, BaseModel


class PurchaseOrderStatus(str, enum.Enum):
    """Represents the current stage of a purchase order."""

    pending = "pending"
    in_progress = "in progress"
    complete = "complete"
    cancelled = "cancelled"


class PurchaseOrder(BaseModel, Base):
    """
    Represents a purchase order record.
    Takes into account that supplier might be different from
    the product brand (i.e the company that manufactured the product).
    """

    __tablename__ = "purchase_orders"

    supplier_name = mapped_column(String(200), unique=True)
    status = mapped_column(
        Enum(PurchaseOrderStatus, name="purchase_order_status", create_type=True),
        default="pending"
    )
    ordering_cost = mapped_column(Float, nullable=False, default=0.00)
    holding_cost_rate = mapped_column(Float, default=0.20)
    employee_id = mapped_column(
        String(36),
        ForeignKey("employees.id", ondelete="SET NULL")
    )

    added_by = relationship("Employee", backref="purchase_orders_added")
    purchases = relationship(
        "Purchase", back_populates="purchase_order"
    )
