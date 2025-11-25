#!/usr/bin/env python3

"""
Routes for managing purchase order items.
"""

from flask import abort, jsonify, request
from typing import Any
import logging

from api.v1.auth.authorization import admin_only
from api.v1.views import app_views
from api.v1.utils.request_data_validation import (
    PurchaseRegister,
    PurchaseUpdate,
    validate_request_data,
)
from api.v1.utils.utility import DatabaseOp, get_obj
from api.v1.views.stock_levels import add_or_subtract_stock
from models import storage
from models.product import Product
from models.purchase_order import PurchaseOrder
from models.purchase import Purchase


logger = logging.getLogger(__name__)


def get_purchase_dict(item: Purchase) -> dict[str, Any]:
    """
    Return purchase order item data excluding relations.
    """
    item_dict = item.to_dict()
    item_dict["product"] = item.product.name
    item_dict["product_quantity_in_stock"] = item.product.quantity_in_stock
    item_dict["added_by"] = item.purchase_order.added_by.username
    item_dict.pop("__class__", None)
    return item_dict


@app_views.route(
    "/purchases",
    strict_slashes=False,
    methods=["POST"],
)
@admin_only
def add_purchase():
    """
    Add a new purchase item.
    """
    valid_data = validate_request_data(PurchaseRegister)

    product = get_obj(Product, valid_data["product_id"])
    if not product:
        abort(404, description="Product does not exist.")

    purchase_order = get_obj(PurchaseOrder, valid_data["purchase_order_id"])
    if not purchase_order:
        abort(404, description="Order does not exist")
    
    purchase = Purchase(**valid_data)

    db = DatabaseOp()
    db.save(purchase)

    # add purchase to stock
    if purchase.item_status == "supplied":
        add_or_subtract_stock(purchase, purchase.product)

    purchase_dict = get_purchase_dict(purchase)
    return jsonify(purchase_dict), 201


@app_views.route(
    "/purchases/<int:page_size>/<int:page_num>",
    strict_slashes=False,
    methods=["GET"]
)
@admin_only
def get_all_purchases(page_size: int, page_num: int):
    """
    Get paginated list of all purchase order items.
    """
    date_time = request.args.get("date_time")

    purchases = storage.all(
        Purchase, page_size=page_size, page_num=page_num, date_time=date_time
    )
    if not purchases:
        abort(404, description="No purchases found")

    purchases_list: list[dict[str, Any]] = [
        get_purchase_dict(purchase) for purchase in purchases
    ]
    return jsonify(purchases_list), 200


@app_views.route(
    "/purchases/<purchase_id>",
    strict_slashes=False,
    methods=["GET"],
)
@admin_only
def get_purchase(purchase_id: str):
    """
    Get a single purchase item by ID.
    """
    purchase= get_obj(Purchase, purchase_id)
    if not purchase:
        abort(404, description="Item does not exist.")

    purchase_dict = get_purchase_dict(purchase)
    return jsonify(purchase_dict), 200


@app_views.route(
    "/purchases/<purchase_id>",
    strict_slashes=False,
    methods=["PUT"],
)
@admin_only
def update_purchase(purchase_id: str):
    """
    Update details of a purchase order item.
    """
    valid_data = validate_request_data(PurchaseUpdate)

    purchase = get_obj(Purchase, purchase_id)
    if not purchase:
        abort(404, description="Item does not exist.")

    if "product_id" in valid_data:
        product = get_obj(Product, valid_data["product_id"])
        if not product:
            abort(404, description="Product does not exist.")

    if "purchase_order_id" in valid_data:
        purchase_order = get_obj(PurchaseOrder, valid_data["purchase_order_id"])
        if not purchase_order:
            abort(404, description="Order does not exist.")

    for attr, value in valid_data.items():
        setattr(purchase, attr, value)

    db = DatabaseOp()
    db.save(purchase)

    # add purchase to stock
    if purchase.item_status == "supplied":
        add_or_subtract_stock(purchase, purchase.product)

    purchase_dict = get_purchase_dict(purchase)
    return jsonify(purchase_dict), 200


@app_views.route(
    "/purchases/<purchase_id>",
    strict_slashes=False,
    methods=["DELETE"],
)
@admin_only
def delete_purchase(purchase_id: str):
    """
    Delete a purchase item.
    """
    purchase = get_obj(Purchase, purchase_id)
    if not purchase:
        abort(404, description="Item does not exist.")

    db = DatabaseOp()
    db.delete(purchase)
    db.commit()
    return jsonify({}), 200
