#!/usr/bin/env python3

"""
Routes for managing sale orders.
"""

from flask import abort, jsonify, g, request
from typing import Any
import logging

from api.v1.auth.authorization import admin_only
from api.v1.views import app_views
from api.v1.utils.request_data_validation import (
    SaleOrderRegister,
    SaleOrderUpdate,
    validate_request_data,
)
from api.v1.utils.utility import DatabaseOp, get_obj
from models import storage
from models.sale_order import SaleOrder


logger = logging.getLogger(__name__)


def get_sale_order_dict(sale_order: SaleOrder) -> dict[str, Any]:
    """
    Return a sale order as a dictionary excluding related items.
    """
    order_dict = sale_order.to_dict()
    order_dict["added_by"] = sale_order.added_by.username
    order_dict.pop("__class__", None)
    return order_dict

def get_sale_order_items_dict(
        sale_order: SaleOrder
    ) -> list[dict[str, Any]]:
    """
    """
    sales: list[dict[str, Any]] = []
    for sale in sale_order.sales:
        sale_dict = sale.to_dict()
        sale_dict["product"] = sale.product.name
        sale.pop("__class__", None)
        sales.append(sale_dict)
    
    return sales

def get_sale_order_items_str(sale_order: SaleOrder) -> list[str]:
    """
    """
    sales: list[str] = [
        f"{sale.product.name}({sale.quantity})"
        for sale in sale_order.sales
    ]
    return sales


@app_views.route("/sale_orders", strict_slashes=False, methods=["POST"])
def register_sale_order():
    """
    Register a new sale order.
    """
    admin = g.current_employee

    valid_data = validate_request_data(SaleOrderRegister)
    valid_data["employee_id"] = admin.id

    sale_order = SaleOrder(**valid_data)

    db = DatabaseOp()
    db.save(sale_order)

    sale_order_dict = get_sale_order_dict(sale_order)
    return jsonify(sale_order_dict), 201


@app_views.route(
    "/sale_orders/<int:page_size>/<int:page_num>",
    strict_slashes=False,
    methods=["GET"],
)
def get_all_sale_orders(page_size: int, page_num: int):
    """
    Get paginated list of all sale orders.
    """
    date_time = request.args.get("date_time")

    sale_orders = storage.all(
        SaleOrder, page_size=page_size, page_num=page_num, date_time=date_time
    )
    if not sale_orders:
        abort(404, description="No sale_order found")

    sale_order_lists: list[dict[str, Any]] = []
    for sale_order in sale_orders:
        order_dict = get_sale_order_dict(sale_order)
        order_dict["sale_order_items"] = get_sale_order_items_dict(
            sale_order)
        order_dict["sale_order_items_summary"] = get_sale_order_items_str(
            sale_order)
        sale_order_lists.append(order_dict)
    
    return jsonify(sale_order_lists), 200


@app_views.route(
    "sale_orders/<sale_order_id>",
    strict_slashes=False,
    methods=["GET"]
)
def get_sale_order(sale_order_id: str):
    """
    Get details of a sale order by ID.
    """
    sale_order = get_obj(SaleOrder, sale_order_id)
    if not sale_order:
        abort(404, description="Order does not exist")

    sale_order_dict = get_sale_order_dict(sale_order)
    sale_order_dict["sale_order_items"] = get_sale_order_items_dict(
        sale_order
    )
    sale_order_dict["sale_order_items_summary"] = get_sale_order_items_str(
        sale_order
    )
    return jsonify(sale_order_dict), 200


@app_views.route(
    "sale_orders/<sale_order_id>",
    strict_slashes=False,
    methods=["PUT"]
)
def update_sale_order(sale_order_id: str):
    """
    Update an existing sale order.
    If status is set to 'complete', all related sales must be paid.
    """
    valid_data = validate_request_data(SaleOrderUpdate)

    sale_order = get_obj(SaleOrder, sale_order_id)
    if not sale_order:
        abort(404, description="Sale_order does not exist")
    
    if valid_data.get("status") == "complete":
        for sale in sale_order.sales:
            if sale and sale.payment_status == "unpaid":
                abort(400, description="Some item(s) have not been paid for.")

    for attr, value in valid_data.items():
        setattr(sale_order, attr, value)

    db = DatabaseOp()
    db.save(sale_order)

    sale_order_dict = get_sale_order_dict(sale_order)
    sale_order_dict.pop("sales", None)

    return jsonify(sale_order_dict), 200


@app_views.route(
    "sale_orders/<sale_order_id>",
    strict_slashes=False,
    methods=["DELETE"]
)
@admin_only
def delete_sale_order(sale_order_id: str):
    """
    Delete a sale order.
    """
    sale_order = get_obj(SaleOrder, sale_order_id)
    if not sale_order:
        abort(404, description="Sale_order does not exist")

    db = DatabaseOp()
    db.delete(sale_order)
    db.commit()
    return jsonify({}), 200
