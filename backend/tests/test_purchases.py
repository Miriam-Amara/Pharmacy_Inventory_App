#!/usr/bin/env python3

"""
Unit tests for the Purchases API endpoints.
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


class TestPurchases(unittest.TestCase):
    """
    Tests the PurchaseOrderItem CRUD and authentication endpoints.

    POST - "/api/v1/purchases"
    GET - "/api/v1/purchases/<int:page_size>/<int:page_num>"
    GET - "/api/v1/purchases/<order_id>/"
    PUT - "/api/v1/purchases/<order_id>/"
    DELETE - "/api/v1/purchases/<order_id>/"
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
        """ """
        self.brand_data = {"name": "Emzor"}
        brand_response = self.client.post(
            "/api/v1/brands",
            json=self.brand_data,
        )
        self.brand_id: str = brand_response.get_json().get("id")

    def delete_brand(self) -> None:
        """ """
        brand: Brand | None = storage.get_obj_by_id(Brand, self.brand_id)
        if not brand:
            raise ValueError("Brand not found")

        storage.delete(brand)
        storage.save()
    
    def add_category(self) -> None:
        """ """
        self.category = {"name": "pain killers"}
        category_response = self.client.post(
            "/api/v1/categories",
            json=self.category,
        )
        self.category_id: str = category_response.get_json().get("id")

    def delete_category(self) -> None:
        """ """
        category: Category | None = storage.get_obj_by_id(Category, self.category_id)
        if not category:
            raise ValueError("Category not found")

        storage.delete(category)
        storage.save()
    
    def add_product(self) -> None:
        """ """
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
        """ """
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

    def setUp(self) -> None:
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
            "item_status": "supplied",
            "payment_status": "paid",
        }
        self.response = self.client.post(
            f"/api/v1/purchases",
            json=self.purchase,
        )
        self.purchase_id = self.response.get_json().get("id")

    def tearDown(self) -> None:
        """
        Deletes the purchase created for each test.
        """
        self.client.delete(
            f"/api/v1/purchases/{self.purchase_id}",
        )
        self.delete_brand()
        self.delete_category()
        self.delete_product()
        self.delete_purchase_order()

        # get and delete stock
        response = self.client.get(f"/api/v1/stock_levels/{5}/{1}")
        logger.debug(f"stock response: {response.get_json()}")
        stock_id = response.get_json()[0].get("id")
        self.client.delete(f"/api/v1/stock_levels/{stock_id}")

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

        db.delete(employee)
        db.commit()

    def test_register_purchase(self):
        """
        Tests successful purchase registration.
        """
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(
            self.response.get_json().get("purchase_order_id"),
            self.purchase_order_id
        )
        self.assertEqual(
            self.response.get_json().get("product_id"),
            self.product_id
        )
        self.assertEqual(
            self.response.get_json().get("quantity"),
            self.purchase["quantity"]
        )
        self.assertEqual(
            self.response.get_json().get("unit_cost_price"),
            self.purchase["unit_cost_price"],
        )
        self.assertEqual(
            self.response.get_json().get("total_cost_price"),
            self.purchase["total_cost_price"],
        )
        self.assertEqual(
            self.response.get_json().get("payment_status"),
            self.purchase["payment_status"].lower(),
        )
        self.assertEqual(
            self.response.get_json().get("product"),
            self.product_data["name"].lower()
        )
        self.assertIn("item_status", self.response.get_json())
        self.assertEqual(len(self.response.get_json()), 13)

    def test_get_all_purchases(self):
        """
        Tests retrieval of all purchases with pagination.
        """
        response = self.client.get(f"/api/v1/purchases/{5}/{1}")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.get_json()), 5)

    def test_get_purchase(self):
        """
        Tests retrieval of a single purchase by ID.
        """
        response = self.client.get(
            f"/api/v1/purchases/{self.purchase_id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.response.get_json().get("purchase_order_id"),
            self.purchase_order_id
        )
        self.assertEqual(
            self.response.get_json().get("product_id"),
            self.product_id
        )
        self.assertEqual(
            self.response.get_json().get("quantity"),
            self.purchase["quantity"]
        )
        self.assertEqual(
            self.response.get_json().get("unit_cost_price"),
            self.purchase["unit_cost_price"],
        )
        self.assertEqual(
            self.response.get_json().get("total_cost_price"),
            self.purchase["total_cost_price"],
        )
        self.assertEqual(
            self.response.get_json().get("payment_status"),
            self.purchase["payment_status"].lower(),
        )
        self.assertEqual(
            self.response.get_json().get("product"),
            self.product_data["name"].lower()
        )
        self.assertIn("item_status", self.response.get_json())
        self.assertEqual(len(self.response.get_json()), 13)

        import json
        logger.debug(json.dumps(self.response.get_json(), indent=4))

    def test_update_purchase(self):
        """
        Tests updating purchase details.
        """
        new_data: dict[str, Any] = {
            "item_status": "supplied",
            "quantity": 4,
            "total_cost_price": 4 * self.purchase["unit_cost_price"],
        }
        response = self.client.put(
            f"/api/v1/purchases/{self.purchase_id}",
            json=new_data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json().get("quantity"),
            new_data["quantity"]
        )
        self.assertEqual(
            response.get_json().get("total_cost_price"),
            new_data["total_cost_price"]
        )

        import json
        logger.debug(json.dumps(response.get_json(), indent=4))


if __name__ == "__main__":
    unittest.main(verbosity=2)
