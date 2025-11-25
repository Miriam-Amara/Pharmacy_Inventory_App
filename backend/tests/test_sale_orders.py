#!/usr/bin/env python3

"""
Unit tests for the SaleOrder API endpoints.
"""

from flask import Flask
from flask.testing import FlaskClient
from typing import Any
import logging
import unittest

from api.v1.app import create_app
from models.employee import Employee
from models.sale_order import SaleOrder


logger = logging.getLogger(__name__)


class TestSaleOrders(unittest.TestCase):
    """
    Tests the Order CRUD and authentication endpoints.

    POST - "/api/v1/sale_orders"
    GET - "/api/v1/sale_orders/<int:page_size>/<int:page_num>"
    GET - "/api/v1/sale_orders/<order_id>"
    PUT - "/api/v1/sale_orders/<order_id>"
    DELETE - "/api/v1/sale_orders/<order_id>"
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
        Creates a new sale order before each test.
        """
        self.response = self.client.post(
            "/api/v1/sale_orders",
            json={"status": "pending"},
        )
        self.order_id = self.response.get_json().get("id")

    def tearDown(self) -> None:
        """
        Deletes the sale order created for each test.
        """
        from api.v1.utils.utility import get_obj, DatabaseOp

        order: SaleOrder | None = get_obj(
            SaleOrder, self.order_id
        )
        if not order:
            raise ValueError("Order not found.")

        db = DatabaseOp()
        db.delete(order)
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

    def test_register_sale_order(self):
        """
        Tests successful sale order registration.
        """
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("status", self.response.get_json())
        self.assertIn("employee_id", self.response.get_json())
        self.assertEqual(
            self.response.get_json().get("added_by"),
            self.employee_data["username"].lower(),
        )
        self.assertEqual(len(self.response.get_json()), 6)

        import json
        logger.debug(f"In register sale: {json.dumps(self.response.get_json(), indent=4)}")

    def test_get_all_sales_orders(self):
        """
        Tests retrieval of all orders with pagination.
        """
        response = self.client.get(f"/api/v1/sale_orders/{5}/{1}")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.get_json()), 5)

        import json
        logger.debug(
            f"In get all sales: {json.dumps(response.get_json(), indent=4)}"
        )

    def test_get_sale_order(self):
        """
        Tests retrieval of a single sale order by ID.
        """
        response = self.client.get(
            f"/api/v1/sale_orders/{self.order_id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.get_json())
        self.assertIn("employee_id", response.get_json())
        self.assertEqual(
            response.get_json().get("added_by"),
            self.employee_data["username"].lower()
        )
        self.assertEqual(len(response.get_json()), 8)

        import json
        logger.debug(f"In get sale: {json.dumps(response.get_json(), indent=4)}")

    def test_update_order(self):
        """
        Tests updating order details.
        """
        response = self.client.put(
            f"/api/v1/sale_orders/{self.order_id}",
            json={"ordering_cost": 2000, "status": "complete"}
        )
        self.assertEqual(response.status_code, 200)

        import json
        logger.debug(f"In update order: {json.dumps(response.get_json(), indent=4)}")

    def test_delete_order(self):
        """
        Tests deleting a sale order record.
        """
        from api.v1.utils.utility import get_obj

        # add a new order
        register_order_response = self.client.post(
            "/api/v1/sale_orders",
            json={"status": "cancelled"},
        )
        order_id = register_order_response.get_json().get("id")

        # delete the new order
        delete_order_response = self.client.delete(
            f"/api/v1/sale_orders/{order_id}"
        )
        self.assertEqual(delete_order_response.status_code, 200)

        order = get_obj(SaleOrder, order_id)
        self.assertIsNone(order)


if __name__ == "__main__":
    unittest.main(verbosity=2)
