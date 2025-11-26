#!/usr/bin/env python3

"""
Routes for managing products.
"""

from flask import abort, jsonify, g, request
from typing import Any
import logging
import os

from api.v1.auth.authorization import admin_only
from api.v1.views import app_views
from api.v1.utils.request_data_validation import (
    ProductRegister,
    ProductUpdate,
    validate_form_data,
)
from api.v1.utils.utility import DatabaseOp, FileManager, get_obj
from models import storage
from models.product import Product
from models.brand import Brand
from models.category import Category


logger = logging.getLogger(__name__)


def get_product_dict(product: Product) -> dict[str, Any]:
    """
    Return product data excluding relations.
    """
    product_dict = product.to_dict()
    product_dict["category_name"] = product.category.name
    product_dict["added_by"] = product.added_by.username
    product_dict["brand_name"] = product.brand.name
    product_dict.pop("image_filepath", None)
    product_dict.pop("__class__", None)
    return product_dict


@app_views.route(
        "/products",
        strict_slashes=False,
        methods=["POST"]
    )
@admin_only
def register_product():
    """
    Create a new product.
    Creates a new brand if brand name is given.
    """
    admin = g.current_employee
    valid_data, image_file = validate_form_data(ProductRegister)
    valid_data["employee_id"] = admin.id

    if not valid_data.get("brand_id") and not valid_data.get("brand_name"):
        abort(400, description="Product must have either brand id or brand name.")

    if valid_data.get("brand_id"):
        # verify existing brand
        brand = get_obj(Brand, valid_data["brand_id"]) 
    else:
        # create new brand
        brand = Brand(name=valid_data["brand_name"], employee_id=admin.id)
    
    if not brand:
        abort(404, description="Brand does not exist.")
    valid_data["brand_id"] = brand.id

    category = get_obj(Category, valid_data["category_id"])
    if not category:
        abort(404, description="Category does not exist.")
    
    if image_file:
        image_filepath = FileManager().process_file(image_file, "products")
        valid_data["image_filepath"] = image_filepath

    product = Product(**valid_data)
    db = DatabaseOp()
    db.save(product)

    product_dict = get_product_dict(product)
    return jsonify(product_dict), 201


@app_views.route(
    "/products/<int:page_size>/<int:page_num>",
    strict_slashes=False,
    methods=["GET"]
)
@admin_only
def get_all_products(page_size: int, page_num: int):
    """
    Get paginated list of products.
    """
    date_time = request.args.get("date_time")
    search_term = request.args.get("search")

    if search_term:
        products = storage.search(
            Product, search_term, page_size=page_size, page_num=page_num
        )
    else:
        products = storage.all(
            Product, page_size=page_size, page_num=page_num, date_time=date_time
        )

    if not products:
        abort(404, description="No product found")

    product_lists: list[dict[str, Any]] = [
        get_product_dict(product) for product in products
    ]

    return jsonify(product_lists), 200


@app_views.route(
        "products/<product_id>",
        strict_slashes=False,
        methods=["GET"]
    )
@admin_only
def get_product(product_id: str):
    """
    Get a single product by ID.
    """
    product = get_obj(Product, product_id)
    if not product:
        abort(404, description="Product does not exist")

    product_dict = get_product_dict(product)
    return jsonify(product_dict), 200


@app_views.route(
        "products/<product_id>",
        strict_slashes=False,
        methods=["PUT"]
    )
@admin_only
def update_product(product_id: str):
    """
    Update product details.
    """
    valid_data, image_file = validate_form_data(ProductUpdate)

    product = get_obj(Product, product_id)
    if not product:
        abort(404, description="Product does not exist")

    if valid_data.get("brand_id"):
        brand = get_obj(Brand, valid_data["brand_id"])
        if not brand:
            abort(404, description="Brand does not exist.")
        valid_data["brand"] = brand

    if valid_data.get("brand_name") and not valid_data.get("brand_id"):
        brand = Brand(name=valid_data["brand_name"])
        valid_data["brand"] = brand

    if "category_id" in valid_data:
        category = get_obj(Category, valid_data["category_id"])
        if not category:
            abort(404, description="Category does not exist.")
        valid_data["category"] = category
    
    if image_file:
        image_filepath = FileManager().process_file(image_file, "products", obj=product)
        valid_data["image_filepath"] = image_filepath

    for attr, value in valid_data.items():
        setattr(product, attr, value)

    db = DatabaseOp()
    db.save(product)

    product_dict = get_product_dict(product)
    return jsonify(product_dict), 200


@app_views.route(
        "products/<product_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
@admin_only
def delete_product(product_id: str):
    """
    Delete a product.
    """
    product = get_obj(Product, product_id)
    if not product:
        abort(404, description="Product does not exist")
    
    image_filepath = product.image_filepath

    if image_filepath:
        absolute_path = os.path.abspath(image_filepath)

        if os.path.exists(absolute_path):
            os.remove(absolute_path)

    db = DatabaseOp()
    db.delete(product)
    db.commit()
    return jsonify({}), 200
