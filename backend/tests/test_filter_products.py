#!/usr/bin/env python3

"""
Unit tests for the Brand API endpoints.
"""

from flask import Flask
from flask.testing import FlaskClient
from typing import Any
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.employee import Employee
from models.brand import Brand
from models.category import Category
from models.product import Product


logger = logging.getLogger(__name__)


class TestFilterProducts(unittest.TestCase):
    """
    Tests the Brand CRUD and authentication endpoints.

    GET - "/api/v1/brands/<brand_id>/products/<int:page_size>/<int:page_num>"
    GET - "/api/v1/categories/<category_id>/products/<int:page_size>/<int:page_num>"
    GET - "/api/v1/categories/<category_id>/brands/<brand_id>/products"
            "/<int:page_size>/<int:page_num>"
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

    def setUp(self) -> None:
        """
        Registers new brands and new products before each test.
        """
        self.brand: dict[str, str] = {"name": "Emzor"}
        self.category: dict[str, str] = {
            "name": "pain killers", "description": "pain relievers"
        }

        self.product_ids: list[str] = []
        self.products: list[dict[str, Any]] = [
            {"name": "Paracetamol", "unit_cost_price": 300, "unit_selling_price": 350},
            {"name": "Panadol", "unit_cost_price": 400, "unit_selling_price": 500},
            {"name": "Lumartem", "unit_cost_price": 500, "unit_selling_price": 1000},
            {"name": "Panadol Extra", "unit_cost_price": 450, "unit_selling_price": 600},
            {"name": "Ibuprofen", "unit_cost_price": 600, "unit_selling_price": 700},
        ]

        brand_response = self.client.post(
            "/api/v1/brands",
            json=self.brand,
        )
        self.brand_id = brand_response.get_json().get("id")

        category_response = self.client.post(
            "/api/v1/categories",
            json=self.category,
        )
        self.category_id = category_response.get_json().get("id")

        for product in self.products:
            product["brand_id"] = self.brand_id
            product["category_id"] = self.category_id

            response = self.client.post(
                "/api/v1/products",
                json=product,
            )
            self.product_ids.append(response.get_json().get("id"))

    def tearDown(self) -> None:
        """
        Deletes the brands and products created for each test.
        """
        brand: Brand | None = storage.get_obj_by_id(Brand, self.brand_id)
        if not brand:
            raise ValueError("Brand not found")
        storage.delete(brand)

        category: Category | None = storage.get_obj_by_id(Category, self.category_id)
        if not category:
            raise ValueError("Category not found")
        storage.delete(category)

        for product_id in self.product_ids:
            product: Product | None = storage.get_obj_by_id(
                Product, product_id
            )
            if not product:
                raise ValueError("Product not found")
            storage.delete(product)

        storage.save()

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

    def test_get_brand_products(self):
        """ """
        response = self.client.get(
            f"/api/v1/brands/{self.brand_id}/products/{5}/{1}"
        )

        brand_products = response.get_json()
        for product in brand_products:
            self.assertEqual(product["brand_name"], self.brand["name"].lower())
    
    def test_get_category_products(self):
        """ """
        response = self.client.get(
            f"/api/v1/categories/{self.category_id}/products/{5}/{1}"
        )

        category_products = response.get_json()
        for product in category_products:
            self.assertEqual(product["category_name"], self.category["name"].lower())

    def test_get_category__brand_products(self):
        """ """
        response = self.client.get(
            f"/api/v1/categories/{self.category_id}/brands/{self.brand_id}/products/{5}/{1}"
        )

        category_brand_products = response.get_json()
        for product in category_brand_products:
            self.assertEqual(product["category_name"], self.category["name"].lower())
            self.assertEqual(product["brand_name"], self.brand["name"].lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
