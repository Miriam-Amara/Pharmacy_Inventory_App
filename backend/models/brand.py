#!/usr/bin/env python3

"""
Brand model and brand-product link table.
"""

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean

from models.basemodel import Base, BaseModel


class Brand(BaseModel, Base):
    """Represents a product brand in the pharmacy."""

    __tablename__ = "brands"

    name = mapped_column(String(200), nullable=False, unique=True)
    is_active = mapped_column(Boolean, default=True)
    employee_id = mapped_column(
        String(36),
        ForeignKey("employees.id", ondelete="SET NULL")
    )
    
    added_by = relationship("Employee", backref="brands")
    products = relationship("Product", back_populates="brand")
