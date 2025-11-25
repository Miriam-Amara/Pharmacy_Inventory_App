#!/usr/bin/env python3

"""
Database storage engine for managing all model interactions.
"""

from datetime import date, datetime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, select, func, extract, desc, or_, and_
from typing import Any, Sequence, Type, TypeVar
import logging

from models.basemodel import Base, BaseModel
from models.brand import Brand
from models.category import Category
from models.employee import Employee
from models.employee_session import EmployeeSession
from models.product import Product
from models.purchase_order import PurchaseOrder
from models.purchase import Purchase
from models.sale_order import SaleOrder
from models.sale import Sale
from models.stock_level import StockLevel


logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class DBStorage:
    """Handles all database operations for the application."""

    __classes: list[Type[BaseModel]] = [
        Brand,
        Category,
        Employee,
        EmployeeSession,
        Product,
        PurchaseOrder,
        Purchase,
        SaleOrder,
        Sale,
        StockLevel,
    ]

    def __init__(self, database_url: str) -> None:
        """Initializes the database engine with the provided URL."""
        self.__engine = create_engine(database_url, pool_pre_ping=True)

    def all(
            self,
            cls: Type[T],
            page_size: int | None = None,
            page_num: int | None = None,
            date_time: str | None = None
        ) -> Sequence[T]:
        """
        Return paginated records of a model, optionally filtered by creation date.

        Args:
            cls: Model class (subclass of BaseModel).
            page_size: Items per page (positive int).
            page_num: Page number (positive int).
            date_time: ISO datetime string to filter by date.

        Raises:
            TypeError, ValueError on invalid inputs.
        """
        if not issubclass(cls, BaseModel):  # type: ignore
            raise TypeError("Cls must inherit from BaseModel")
        if (
            page_size
            and (isinstance(page_size, bool)
            or not isinstance(page_size, int) # type:ignore
            or page_size <= 0)
        ):
            raise TypeError("Page size must be a valid positive integer")
        if (
            page_num
            and (isinstance(page_num, bool)
            or not isinstance(page_num, int) # type: ignore
            or page_num <= 0)
        ):
            raise TypeError("Page number must be a valid positive integer")
        if date_time:
            try:
                datetime.fromisoformat(date_time)
            except ValueError:
                raise ValueError("date_time must be a valid ISO datetime string")

        stmt = select(cls)

        if date_time:
            date_only: date = datetime.fromisoformat(date_time).date()
            stmt = stmt.where(func.date(cls.created_at) == date_only)
        if page_size and page_num:
            stmt = stmt.offset((page_num - 1) * page_size).limit(page_size)
        
        cls_objects = self.__session.scalars(stmt).all()

        return cls_objects
    
    def count(self, cls: Type[T] | None = None) -> int | dict[str, Any] | None:
        """Returns the count of records for a model or all models."""
        if cls in self.__classes:
            count_cls_objects: int | None = self.__session.scalar(
                select(func.count()).select_from(cls)
            )
            return count_cls_objects

        count_all_objects: dict[str, Any] = {}
        for cls_name in self.__classes:
            count_cls_obj = self.__session.scalar(
                select(func.count()).select_from(cls_name)
            )
            count_all_objects[cls_name.__name__] = count_cls_obj
        return count_all_objects

    def close(self):
        """Closes the current database session."""
        self.__session.close()

    def delete(self, obj: BaseModel) -> None:
        """Deletes an object from the current session."""
        self.__session.delete(obj)

    def filter_products(
            self,
            page_size: int,
            page_num: int,
            brand_id: str | None = None,
            category_id: str | None = None,
            filter_type: str | None = None) -> Sequence[Product]:
        """
        Filter products by category or brand or both.
        """
        stmt = select(Product)
        if filter_type == "brand" and brand_id:
            stmt = stmt.where(Product.brand_id == brand_id)
        elif filter_type == "category" and category_id:
            stmt = stmt.where(Product.category_id == category_id)
        else:
            stmt = stmt.where(and_(
                Product.brand_id == brand_id,
                Product.category_id == category_id
            ))
        
        stmt = stmt.offset((page_num - 1) * page_size).limit(page_size)
        products = self.__session.scalars(stmt).all()
        return products

    def get_obj_by_id(self, cls: Type[T], id: str) -> T | None:
        """Fetches a single object by its ID."""
        if issubclass(cls, BaseModel):  # type: ignore
            obj = self.__session.get(cls, id)
            return obj
    
    def get_stock_obj(self, product_id: str) -> StockLevel | None:
        """Fetches a single stock level object by the given product id."""
        stock = self.__session.scalars(
            select(StockLevel).where(StockLevel.product_id == product_id)
        ).one_or_none()
        return stock

    def new(self, obj: BaseModel):
        """Adds a new object to the current session."""
        self.__session.add(obj)

    def reload(self):
        """Creates all tables and initializes a scoped session."""
        # Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )

    def save(self):
        """Commits all pending changes to the database."""
        try:
            self.__session.commit()
        except Exception as e:
            try:
                self.__session.rollback()
            except Exception as rollback_error:
                logger.critical(f"Rollback failed: {rollback_error}")
            raise e
    
    def search(
            self,
            cls: Type[T],
            search_term: str,
            page_size: int | None = None,
            page_num: int | None = None,
        ) -> Sequence[T]:
        """
        Search Brand, Category, Product for a match of the given search term.
        """
        if not issubclass(cls, BaseModel):  # type: ignore
            raise TypeError("Cls must inherit from BaseModel")
        
        if (
            not isinstance(search_term, str)  # type: ignore
            or not search_term.strip()
        ):
            raise ValueError("search_term must be an instance of str.")
        if (
            page_size
            and (isinstance(page_size, bool)
            or not isinstance(page_size, int) # type:ignore
            or page_size <= 0)
        ):
            raise TypeError("Page size must be a valid positive integer")
        if (
            page_num
            and (isinstance(page_num, bool)
            or not isinstance(page_num, int) # type: ignore
            or page_num <= 0)
        ):
            raise TypeError("Page number must be a valid positive integer")
        
        
        stmt = select(cls).where(cls.name.ilike(f"%{search_term}%")) # type: ignore

        if page_size and page_num:
            stmt = stmt.limit(page_size).offset((page_num - 1) * page_size)

        cls_objects = self.__session.scalars(stmt).all()
        return cls_objects


    def search_employee_by_email_username(
        self, email_or_username: str
    ) -> Employee | None:
        """Finds an employee by email or username."""
        if not email_or_username or not email_or_username.strip():
            raise ValueError("Either email or username is required")

        employee = self.__session.scalars(
            select(Employee)
            .where(or_(
                Employee.email == email_or_username,
                Employee.username == email_or_username
            ))
            ).one_or_none()
        
        return employee
    
    def search_product_by_barcode(self, barcode: str) -> Product | None:
        """Finds a product by barcode"""
        product = self.__session.scalars(
            select(Product).where(Product.barcode == barcode)
        ).one_or_none()
        return product
    
    # def record_stock(
    #     self,
    #     product_id: str,
    #     quantity: int,
    #     operation: str
    # ) -> StockLevel | None:
    #     """
    #     """
    #     if not product_id or not quantity or not operation:
    #         return
        
    #     if quantity <= 0:
    #         return
        
    #     if operation.lower() not in ["add", "subtract"]:
    #         return
        
    #     stock: StockLevel | None = self.__session.scalars(
    #         select(StockLevel).where(StockLevel.product_id == product_id)
    #     ).one_or_none()
        
    #     if not stock:
    #         return
        
    #     if operation.lower() == "add":
    #         stock.quantity_in_stock += quantity
    #         return
    
    #     if stock.quantity_in_stock < 0:
    #         raise ValueError("Insufficient stock")
        
    #     stock.quantity_in_stock -= quantity
    #     return stock

    # def get_monthly_sales_summary(
    #     self,
    #     product_id: str,
    #     year: int,
    #     month: int
    # ) -> dict[str, Any]:
    #     """
    #     Returns total quantity and total selling price for a product and brand
    #     within a given month. If no sales exist, returns both totals as 0.
    #     """
    #     result = (
    #         self.__session.query(
    #             func.coalesce(func.sum(Sale.quantity), 0)
    #             .label("total_quantity"),
    #             func.coalesce(func.sum(Sale.total_selling_price), 0)
    #             .label("total_selling_price")
    #         )
    #         .filter(
    #             Sale.product_id == product_id,
    #             extract("year", Sale.created_at) == year, # type: ignore
    #             extract("month", Sale.created_at) == month # type: ignore
    #         )
    #         .one()
    #     )

    #     return {
    #         "total_quantity": int(result.total_quantity),
    #         "total_selling_price": float(result.total_selling_price),
    #     }
    

    # def get_lead_time(self, product_id: str, brand_id: str) -> int | None:
    #     """
    #     Calculate lead time for the last purchase for a product and brand.
    #     Lead time = last_updated - created_at.
    #     Returns None if no purchase found for the product and brand.
    #     """
    #     last_purchase = (
    #         self.__session.query(Purchase)
    #         .filter(
    #             Purchase.product_id == product_id,
    #             Purchase.purchase_order.brand_id == brand_id,
    #             Purchase.item_status == "supplied"
    #         )
    #         .order_by(desc(Purchase.last_updated))  # type: ignore
    #         .first()
    #     )

    #     if last_purchase is None:
    #         return None

    #     lead_time = last_purchase.last_updated - last_purchase.created_at
    #     return lead_time.days

    # def get_last_month_reordering_point(self, product_id: str):
    #     """
    #     Retrieve the latest reordering point record for the given brand & product.
    #     Returns 0 if not found.
    #     """
    #     if not product_id:
    #         return 0

    #     reordering_point = self.__session.scalar(
    #         select(ReorderingPoint)
    #         .where(
    #             ReorderingPoint.product_id == product_id
    #         )
    #     )

    #     if not reordering_point:
    #         return 0
    #     return reordering_point.reordering_quantity


    # def get_daily_demand_stats(self, product_id: int, brand_id: int, year: int, month: int):
    #     """
    #     Calculate average daily demand and std deviation of daily demand
    #     from sales data within a specified month.
    #     """

    #     # Query: group sales by date and sum quantity per day
    #     daily_sales = (
    #         self.__session.query(
    #             cast(Sale.created_at, Date).label("sale_date"),
    #             func.sum(Sale.quantity).label("total_quantity")
    #         )
    #         .filter(
    #             Sale.product_id == product_id,
    #             Sale.brand_id == brand_id,
    #             func.extract("year", Sale.created_at) == year, # type: ignore
    #             func.extract("month", Sale.created_at) == month # type: ignore
    #         )
    #         .group_by("sale_date")
    #         .order_by("sale_date")
    #         .all()
    #     )

    #     if not daily_sales:
    #         return 0.0, 0.0  # no sales data

    #     quantities = [row.total_quantity for row in daily_sales]
    #     avg_daily_demand = np.mean(quantities)
    #     std_dev_daily_demand = np.std(quantities, ddof=1)  # sample std dev

    #     return avg_daily_demand, std_dev_daily_demand


    # def get_lead_time_stats(self, product_id: int, brand_id: int):
    #     """
    #     Calculate average and standard deviation of lead times (in days)
    #     for purchase order items of a product-brand.
    #     """
    #     lead_times_query = (
    #         self.__session.query(
    #             (
    #                 func.julianday(Purchase.last_updated)
    #                 - func.julianday(Purchase.created_at)
    #             ).label("lead_time_days")
    #         )
    #         .filter(
    #             Purchase.product_id == product_id,
    #             Purchase.purchase_order.brand_id == brand_id,
    #             Purchase.last_updated.isnot(None),
    #             Purchase.created_at.isnot(None)
    #         )
    #         .all()
    #     )

    #     if not lead_times_query:
    #         return 0.0, 0.0

    #     lead_times = [row.lead_time_days for row in lead_times_query]
    #     avg_lead_time = np.mean(lead_times)
    #     std_dev_lead_time = np.std(lead_times, ddof=1)  # sample std dev

    #     return avg_lead_time, std_dev_lead_time
    

    # def calculate_safety_stock_from_db(
    #         self,
    #         product_id: int,
    #         brand_id: int,
    #         year: int,
    #         month: int, service_level_percent: float
    #     ):
    #     avg_daily_demand, std_dev_daily_demand = self.get_daily_demand_stats(
    #         product_id, brand_id, year, month
    #     )
    #     avg_lead_time, std_dev_lead_time = self.get_lead_time_stats(
    #         product_id, brand_id
    #     )

    #     if avg_daily_demand == 0 or avg_lead_time == 0:
    #         return 0.0  # insufficient data to calculate safety stock

    #     safety_stock = calculate_safety_stock(
    #         avg_daily_demand,
    #         std_dev_daily_demand,
    #         avg_lead_time,
    #         std_dev_lead_time,
    #         service_level_percent
    #     )
    #     return safety_stock
