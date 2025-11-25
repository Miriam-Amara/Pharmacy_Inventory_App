#!/usr/bin/python3

"""
"""

from flask import abort, jsonify, request
from typing import Any
import logging

from api.v1.auth.authorization import admin_only
from api.v1.views import app_views
from api.v1.utils.request_data_validation import (
    StockLevelUpdate,
    validate_request_data,
)
from api.v1.utils.utility import DatabaseOp, get_obj
from models import storage
from models.product import Product
from models.purchase import Purchase
from models.sale import Sale
from models.stock_level import StockLevel


logger = logging.getLogger(__name__)


def get_stock_level_dict(stock: StockLevel) -> dict[str, Any]:
    """
    """
    stock_dict = stock.to_dict()
    if stock.product:
        logger.debug(f"stock product: {stock.product}")
        stock_dict["product_name"] = stock.product.name
    stock_dict.pop("__class__", None)

    return stock_dict


def add_or_subtract_stock(obj: Purchase | Sale, product: Product) -> None:
    """
    Automatically updates stock levels after a purchase or sale.
    """
    if obj.quantity <= 0:
        abort(400, description="Quantity must be greater than 0.")

    stock: StockLevel | None = storage.get_stock_obj(product.id)

    if stock: 
        if isinstance(obj, Purchase):
            stock.quantity_in_stock += obj.quantity
        elif isinstance(obj, Sale):  # type: ignore
            if obj.quantity > stock.quantity_in_stock:
                abort(400, description="Not enough stock available.")
            stock.quantity_in_stock -= obj.quantity

    else:
        if isinstance(obj, Sale):
            abort(400, description="No available stock to substract sales from.")
        stock = StockLevel(
            product_id=product.id, quantity_in_stock=obj.quantity
        )

    db = DatabaseOp()

    product.quantity_in_stock = stock.quantity_in_stock
    db.save(stock)
    db.save(product)


@app_views.route(
    "/stock_levels/<stock_level_id>",
    strict_slashes=False,
    methods=["GET"])
@admin_only
def get_stock_level(stock_level_id: str):
    """
    """
    stock = get_obj(StockLevel, stock_level_id)
    if not stock:
        abort(404, description="No stock found")
    
    return jsonify(get_stock_level_dict(stock)), 200


@app_views.route(
    "/stock_levels/<int:page_size>/<int:page_num>",
    strict_slashes=False,
    methods=["GET"]
)
@admin_only
def get_all_current_stock(page_size: int, page_num: int):
    """
    """
    date_time = request.args.get("date_time")

    stock_levels = storage.all(
        StockLevel, page_size=page_size, page_num=page_num, date_time=date_time
    )
    if not stock_levels:
        abort(404, description="No stock found")
    
    all_stocks: list[dict[str, Any]] = [
        get_stock_level_dict(stock) for stock in stock_levels
    ]
    return jsonify(all_stocks), 200


@app_views.route(
    "stock_levels/<stock_level_id>",
    strict_slashes=False,
    methods=["PUT"]
)
@admin_only
def update_stock_level(stock_level_id: str):
    """
    Allows admin to update stock.
    """
    valid_data = validate_request_data(StockLevelUpdate)

    if "product_id" in valid_data:
        product = get_obj(Product, valid_data["product_id"])
        if not product:
            abort(404, description="Product does not exist.")

    stock = get_obj(StockLevel, stock_level_id)
    if not stock:
        abort(404, description="Stock does not exist")
    
    for attr, value in valid_data.items():
        setattr(stock, attr, value)
    
    db = DatabaseOp()
    db.save(stock)

    return jsonify(get_stock_level_dict(stock)), 200

@app_views.route(
    "stock_levels/<stock_level_id>",
    strict_slashes=False,
    methods=["DELETE"]
)
@admin_only
def delete_stock_level(stock_level_id: str):
    """
    Allows admin to delete stock.
    """
    stock = get_obj(StockLevel, stock_level_id)
    if not stock:
        abort(404, description="Stock does not exist")
    
    db = DatabaseOp()
    db.delete(stock)
    db.commit()

    return jsonify({}), 200
