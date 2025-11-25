#!/usr/bin/env python3

"""
Unit tests for the stock level API endpoints.
"""

from flask import Flask
from flask.testing import FlaskClient
from typing import Any
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.brand import Brand
from models.category import Category
from models.employee import Employee
from models.product import Product
from models.purchase_order import PurchaseOrder


logger = logging.getLogger(__name__)


class TestStockLevels(unittest.TestCase):
    """
    Tests the stock levels CRUD and authentication endpoints.

    GET - "/api/v1/stock_levels/<int:page_size>/<int:page_num>"
    GET - "/api/v1/stock_levels/<stock_level_id>"
    PUT - "/api/v1/stock_levels/<stock_level_id>"
    DELETE - "/api/v1/stock_levels/<stock_level_id>"
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up the test app and logs in an admin user.
        """
        cls.app: Flask = create_app()
        cls.client: FlaskClient = cls.app.test_client()

        cls.employee_data: dict[str, Any] = {
            "first_name": "Range",
            "last_name": "Rover",
            "username": "RRover",
            "email": "rangerover@gmail.com",
            "password": "Ranger1234",
            "home_address": "No. 1 sporty street",
            "role": "Manager",
            "is_admin": True,
        }

        cls.client.post(
            "/api/v1/register",
            json=cls.employee_data,
        )
        response = cls.client.post(
            "/api/v1/auth_session/login",
            json={"email_or_username": "RRover", "password": "Ranger1234"},
        )
        cls.employee_id = response.get_json().get("employee_id")

        session_cookie = response.headers.get("Set-Cookie")
        if session_cookie:
            cookie_name, session_id = (
                session_cookie.split(";", 1)[0].split("=", 1)
            )
            cls.client.set_cookie(cookie_name, session_id)

    def add_brand(self) -> None:
        """ Create a new brand before each test. """
        self.brand_data = {"name": "Emzor"}
        brand_response = self.client.post(
            "/api/v1/brands",
            json=self.brand_data,
        )
        self.brand_id: str = brand_response.get_json().get("id")

    def delete_brand(self) -> None:
        """ Delete brand after each test. """
        brand: Brand | None = storage.get_obj_by_id(Brand, self.brand_id)
        if not brand:
            raise ValueError("Brand not found")

        storage.delete(brand)
        storage.save()
    
    def add_category(self) -> None:
        """ Create a new category before each test. """
        self.category = {"name": "pain killers"}
        category_response = self.client.post(
            "/api/v1/categories",
            json=self.category,
        )
        self.category_id: str = category_response.get_json().get("id")

    def delete_category(self) -> None:
        """ Delete category after each test. """
        category: Category | None = storage.get_obj_by_id(Category, self.category_id)
        if not category:
            raise ValueError("Category not found")

        storage.delete(category)
        storage.save()
    
    def add_product(self) -> None:
        """ Create a new product before each test. """
        self.add_brand()
        self.add_category()

        self.product_data: dict[str, Any] = {
            "name": "Paracetamol",
            "brand_id": self.brand_id,
            "category_id": self.category_id,
            "unit_cost_price": 250,
            "unit_selling_price": 350,
        }
        response = self.client.post(
            "/api/v1/products",
            json=self.product_data,
        )
        self.product_id = response.get_json().get("id")

    def delete_product(self) -> None:
        """ Delete product after each test. """
        product: Product | None = storage.get_obj_by_id(
            Product, self.product_id
        )
        if not product:
            raise ValueError("Product not found")

        storage.delete(product)
        storage.save()

    def add_purchase_order(self) -> None:
        """ """
        self.purchase_order: dict[str, Any] = {
            "supplier": "uuuuurr", "ordering_cost": 3000
        }
        response = self.client.post(
            "/api/v1/purchase_orders",
            json=self.purchase_order,
        )
        self.purchase_order_id: str = response.get_json().get("id")

    def delete_purchase_order(self) -> None:
        """ """
        order: PurchaseOrder | None = storage.get_obj_by_id(
            PurchaseOrder, self.purchase_order_id
        )
        if not order:
            raise ValueError("Order not found")

        storage.delete(order)
        storage.save()

    def add_purchase(self) -> None:
        """
        Registers a new purchase before each test.
        """
        self.add_product()
        self.add_purchase_order()

        self.purchase: dict[str, Any] = {
            "product_id": self.product_id,
            "purchase_order_id": self.purchase_order_id,
            "quantity": 2,
            "unit_cost_price": 200,
            "total_cost_price": 400,
            "payment_status": "paid",
            "item_status": "supplied",
        }
        self.purchase_response = self.client.post(
            f"/api/v1/purchases",
            json=self.purchase,
        )
        self.purchase_id = self.purchase_response.get_json().get("id")

    def delete_purchase(self) -> None:
        """
        Deletes the purchase created for each test.
        """
        self.client.delete(
            f"/api/v1/purchases/{self.purchase_id}",
        )
    
    def setUp(self) -> None:
        """ Sets up purchases before each tests. """
        self.add_purchase()

    def tearDown(self) -> None:
        """ Deletes items after each test """
        self.delete_brand()
        self.delete_category()
        self.delete_product()
        self.delete_purchase_order()
        self.delete_purchase()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Deletes the admin user created for the test class.
        """
        from api.v1.utils.utility import get_obj, DatabaseOp

        db = DatabaseOp()

        employee = get_obj(Employee, cls.employee_id)
        if not employee:
            raise ValueError("employee not found")
        employee.delete()
        db.commit()

    def test_get_all_current_stock(self):
        """
        """
        response = self.client.get(f"/api/v1/stock_levels/{5}/{1}")
        self.assertEqual(response.status_code, 200)

        # delete stock
        stock_id = response.get_json()[0].get("id")
        delete_response = self.client.delete(f"/api/v1/stock_levels/{stock_id}")
        self.assertEqual(delete_response.status_code, 200)

    def test_update_stock(self):
        """
        """
        # get all stock
        get_response = self.client.get(f"/api/v1/stock_levels/{5}/{1}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.get_json()[0].get("quantity_in_stock"), 2)

        stock_id = get_response.get_json()[0].get("id")

        # update stock
        update_response = self.client.put(
            f"/api/v1/stock_levels/{stock_id}",
            json={"quantity_in_stock": 6}
            )
        logger.debug(f"update response: {update_response.get_json()}")
        self.assertEqual(update_response.get_json().get("quantity_in_stock"), 6)

        # delete stock
        delete_response = self.client.delete(f"/api/v1/stock_levels/{stock_id}")
        self.assertEqual(delete_response.status_code, 200)
