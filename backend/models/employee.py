#!/usr/bin/env python3

"""
Employee model.
"""

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Boolean

from models.basemodel import Base, BaseModel


class Employee(BaseModel, Base):
    """Represents an employee in the system."""

    __tablename__ = "employees"

    first_name = mapped_column(String(200), nullable=False)
    middle_name = mapped_column(String(200))
    last_name = mapped_column(String(200), nullable=False)
    username = mapped_column(String(200), unique=True)
    email = mapped_column(String(200), unique=True)
    password = mapped_column(String(200), nullable=False)
    home_address = mapped_column(String(500), nullable=False)
    role = mapped_column(String(200), nullable=False)
    image_url = mapped_column(String(100), unique=True)
    is_admin = mapped_column(Boolean, default=False)

    employee_session = relationship(
        "EmployeeSession",
        back_populates="employee",
        cascade="all, delete-orphan"
    )

    @classmethod
    def search_employee_by_email_username(
        cls,
        email_or_username: str,
    ):
        """Find an employee by email or username."""
        from models import storage

        return storage.search_employee_by_email_username(email_or_username)
