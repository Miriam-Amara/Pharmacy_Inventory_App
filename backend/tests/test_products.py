#!/usr/bin/env python3

"""
Unit tests for the Product API endpoints.
"""

from flask import Flask
from flask.testing import FlaskClient
from PIL import Image
from typing import Any, Tuple
import io
import logging
import unittest

from api.v1.app import create_app
from models.employee import Employee
from models.product import Product
from models.brand import Brand
from models.category import Category


logger = logging.getLogger(__name__)


class TestProducts(unittest.TestCase):
    """
    Tests the Product CRUD and authentication endpoints.

    POST - "/api/v1/products"
    GET - "/api/v1/products/<int:page_size>/<int:page_num>"
    GET - "/api/v1/products/<product_id>"
    PUT - "/api/v1/products/<product_id>"
    DELETE - "/api/v1/products/<product_id>"
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
    

    def generate_test_image(
            self,
            format: str="JPEG",
            color: Tuple[int, int, int]=(255, 0, 0)
        ):
        """
        """
        if color:
            img = Image.new("RGB", (200, 200), color=color)
        else:
            img = Image.new("RGB", (200, 200), color=(255, 0, 0))
        buf = io.BytesIO()
        img.save(buf, format=format)
        buf.seek(0)
        return buf


    def setUp(self) -> None:
        """
        Registers a new product before each test.
        """
        # register category
        self.category_data: dict[str, Any] = {"name": "pain killers"}
        self.category_response = self.client.post(
            "/api/v1/categories",
            json=self.category_data,
        )

        self.category_id = self.category_response.get_json().get("id")

        # register product
        self.product_data: dict[str, Any] = {
            "image": "",
            "name": "Paracetamol",
            "category_id": self.category_id,
            "brand_name": "Emzor",
            "unit_cost_price": 250,
            "unit_selling_price": 350,
        }
    
        self.product_data["image"] = (self.generate_test_image("JPEG"), "test.jpg")

        self.response = self.client.post(
            "/api/v1/products",
            data=self.product_data,
            content_type="multipart/form-data"
        )
        self.product_id = self.response.get_json().get("id")
        self.brand_id = self.response.get_json().get("brand_id")

    def tearDown(self) -> None:
        """
        Deletes the product created for each test.
        """
        from api.v1.utils.utility import get_obj, DatabaseOp

        self.client.delete(f"/api/v1/products/{self.product_id}")

        category = get_obj(Category, self.category_id)
        if not category:
            raise ValueError("Category not found")
        
        brand = get_obj(Brand, self.brand_id)
        if not brand:
            raise ValueError("Brand not found")

        db = DatabaseOp()
        brand.delete()
        category.delete()
        db.commit()

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

    def test_register_products(self):
        """
        Tests successful product registration.
        """
        logger.debug(self.response.get_json())
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("name", self.response.get_json())
        self.assertIn("unit_selling_price", self.response.get_json())
        self.assertNotIn("image_filepath", self.response.get_json())
        self.assertNotIn("__class__", self.response.get_json())
        self.assertEqual(
            self.category_data["name"].lower(),
            self.response.get_json().get("category_name")
        )
        self.assertEqual(
            self.employee_data["username"].lower(),
            self.response.get_json().get("added_by"),
        )

    def test_get_all_products(self):
        """
        Tests retrieval of all products with pagination.
        """
        response = self.client.get(f"/api/v1/products/{5}/{1}")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.get_json()), 5)
        

    def test_get_product(self):
        """
        Tests retrieval of a single product by ID.
        """
        response = self.client.get(
            f"/api/v1/products/{self.product_id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json().get("name"),
            self.product_data["name"].lower(),
        )
        self.assertEqual(len(response.get_json()), 25)

    def test_update_product(self):
        """
        Tests updating product details.
        """
        new_data: dict[str, Any] = {
            "name": "Panadol",
            "unit_selling_price": 500.00
        }
        response = self.client.put(
            f"/api/v1/products/{self.product_id}",
            json=new_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json().get("name"),
            new_data["name"].lower()
        )
        self.assertEqual(
            response.get_json().get("unit_selling_price"),
            new_data["unit_selling_price"]
        )
        self.assertEqual(
            response.get_json().get("category_id"),
            self.product_data["category_id"]
        )

        image_file = {
            "image": (self.generate_test_image("JPEG", color=(50, 60, 30)), "test2.jpg")
        }
        response = self.client.put(
            f"/api/v1/products/{self.product_id}",
            data=image_file,
            content_type="multipart/form-data"

        )
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        """
        Tests deleting a product record.
        """
        from api.v1.utils.utility import get_obj

        product_data: dict[str, Any] = {
            "name": "ampiclox",
            "unit_cost_price": "250",
            "unit_selling_price": "400",
            "category_id": self.category_id,
            "brand_id": self.brand_id,
        }
        register_response = self.client.post(
            "/api/v1/products",
            json=product_data,
        )

        product_id = register_response.get_json().get("id")

        response = self.client.delete(f"/api/v1/products/{product_id}")
        self.assertEqual(response.status_code, 200)

        product = get_obj(Product, product_id)
        self.assertIsNone(product)


if __name__ == "__main__":
    unittest.main(verbosity=2)
