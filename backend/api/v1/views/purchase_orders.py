#!/usr/bin/env python3

"""
Routes for managing purchase orders.
"""

from flask import abort, jsonify, g, request
from typing import Any
import logging

from api.v1.auth.authorization import admin_only
from api.v1.views import app_views
from api.v1.utils.request_data_validation import (
    PurchaseOrderRegister,
    PurchaseOrderUpdate,
    validate_request_data,
)
from api.v1.utils.utility import DatabaseOp, get_obj
from models import storage
from models.purchase_order import PurchaseOrder


logger = logging.getLogger(__name__)


def get_purchase_order_dict(purchase_order: PurchaseOrder) -> dict[str, Any]:
    """
    Return a purchase order as a dictionary excluding related items.
    """
    order_dict = purchase_order.to_dict()
    order_dict["added_by"] = purchase_order.added_by.username
    order_dict.pop("__class__", None)
    return order_dict

def get_purchase_order_items_dict(
        purchase_order: PurchaseOrder
    ) -> list[dict[str, Any]]:
    """
    """
    purchases: list[dict[str, Any]] = []
    for purchase in purchase_order.purchases:
        purchase_dict = purchase.to_dict()
        purchase_dict["product"] = purchase.product.name
        purchase.pop("__class__", None)
        purchases.append(purchase_dict)
    
    return purchases

def get_purchase_order_items_str(purchase_order: PurchaseOrder) -> list[str]:
    """
    """
    purchases: list[str] = [
        f"{purchase.product.name}({purchase.quantity})"
        for purchase in purchase_order.purchases
    ]
    return purchases


@app_views.route("/purchase_orders", strict_slashes=False, methods=["POST"])
@admin_only
def register_purchase_order():
    """
    Register a new purchase order.
    """
    admin = g.current_employee

    valid_data = validate_request_data(PurchaseOrderRegister)
    valid_data["employee_id"] = admin.id

    purchase_order = PurchaseOrder(**valid_data)

    db = DatabaseOp()
    db.save(purchase_order)

    purchase_order_dict = get_purchase_order_dict(purchase_order)
    return jsonify(purchase_order_dict), 201


@app_views.route(
    "/purchase_orders/<int:page_size>/<int:page_num>",
    strict_slashes=False,
    methods=["GET"],
)
@admin_only
def get_all_purchase_orders(page_size: int, page_num: int):
    """
    Get paginated list of all purchase orders.
    """
    date_time = request.args.get("date_time")

    purchase_orders = storage.all(
        PurchaseOrder, page_size=page_size, page_num=page_num, date_time=date_time
    )
    if not purchase_orders:
        abort(404, description="No purchase_order found")

    purchase_order_lists: list[dict[str, Any]] = [
        get_purchase_order_dict(purchase_order) for purchase_order in purchase_orders
    ]
    return jsonify(purchase_order_lists), 200


@app_views.route(
    "purchase_orders/<purchase_order_id>",
    strict_slashes=False,
    methods=["GET"]
)
@admin_only
def get_purchase_order(purchase_order_id: str):
    """
    Get details of a purchase order by ID.
    """
    purchase_order = get_obj(PurchaseOrder, purchase_order_id)
    if not purchase_order:
        abort(404, description="Order does not exist")

    purchase_order_dict = get_purchase_order_dict(purchase_order)
    purchase_order_dict["purchase_order_items"] = get_purchase_order_items_dict(
        purchase_order
    )
    purchase_order_dict["purchase_order_items_summary"] = get_purchase_order_items_str(
        purchase_order
    )
    return jsonify(purchase_order_dict), 200


@app_views.route(
    "purchase_orders/<purchase_order_id>",
    strict_slashes=False,
    methods=["PUT"]
)
@admin_only
def update_purchase_order(purchase_order_id: str):
    """
    Update an existing purchase order.
    """
    valid_data = validate_request_data(PurchaseOrderUpdate)

    purchase_order = get_obj(PurchaseOrder, purchase_order_id)
    if not purchase_order:
        abort(404, description="Purchase_order does not exist")

    for attr, value in valid_data.items():
        setattr(purchase_order, attr, value)

    db = DatabaseOp()
    db.save(purchase_order)

    purchase_order_dict = get_purchase_order_dict(purchase_order)
    return jsonify(purchase_order_dict), 200


@app_views.route(
    "purchase_orders/<purchase_order_id>",
    strict_slashes=False,
    methods=["DELETE"]
)
@admin_only
def delete_purchase_order(purchase_order_id: str):
    """
    Delete a purchase order.
    """
    purchase_order = get_obj(PurchaseOrder, purchase_order_id)
    if not purchase_order:
        abort(404, description="Purchase_order does not exist")

    db = DatabaseOp()
    db.delete(purchase_order)
    db.commit()
    return jsonify({}), 200
