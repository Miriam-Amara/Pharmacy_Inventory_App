#!/usr/bin/env python3

"""
Defines routes for brand management operations.
"""

from flask import abort, jsonify
from typing import Any
import logging

from api.v1.auth.authorization import admin_only
from api.v1.views import app_views
from api.v1.utils.utility import get_obj
from models import storage
from models.brand import Brand
from models.category import Category
from models.product import Product


logger = logging.getLogger(__name__)


def get_product_dict(product: Product) -> dict[str, Any]:
    """
    Return product dicts.
    """
    product_dict = product.to_dict()
    product_dict["category_name"] = product.category.name
    product_dict["added_by"] = product.added_by.username
    product_dict["brand_name"] = product.brand.name
    product_dict.pop("image_filepath", None)
    product_dict.pop("__class__", None)
    return product_dict


@app_views.route(
        "brands/<brand_id>/products/<int:page_size>/<int:page_num>",
        strict_slashes=False,
        methods=["GET"]
    )
@admin_only
def get_brand_products(brand_id: str, page_size: int, page_num: int):
    """
    "Get all products linked to a brand.
    """
    brand = get_obj(Brand, brand_id)
    if not brand:
        abort(404, description="Brand does not exist.")

    brand_products = storage.filter_products(
        page_size,
        page_num,
        brand_id=brand.id,
        filter_type="brand"
    )
    if not brand_products:
        abort(404, description="No product found for the brand.")

    brand_products_list = [
        get_product_dict(product) for product in brand_products
    ]
    return jsonify(brand_products_list), 200


@app_views.route(
    "categories/<category_id>/products/<int:page_size>/<int:page_num>",
    strict_slashes=False,
    methods=["GET"]
)
@admin_only
def get_category_products(category_id: str, page_size: int, page_num: int):
    """
    Get all products linked to a category.
    """
    category = get_obj(Category, category_id)
    if not category:
        abort(404, description="Category does not exist.")
    
    category_products = storage.filter_products(
        page_size,
        page_num,
        category_id=category.id,
        filter_type="category"
    )
    if not category_products:
        abort(404, description="No product found for the category.")
    
    category_products_list = [
        get_product_dict(product) for product in category_products
    ]
    return jsonify(category_products_list), 200


@app_views.route(
        "categories/<category_id>/brands/<brand_id>/products/<int:page_size>/<int:page_num>",
        strict_slashes=False,
        methods=["GET"]
    )
def get_category_brand_products(
    category_id: str, brand_id: str, page_size: int, page_num: int
):
    """
    Get all products linked to a category and brand.
    """
    category = get_obj(Category, category_id)
    if not category:
        abort(404, description="Category does not exist.")
    
    brand = get_obj(Brand, brand_id)
    if not brand:
        abort(404, description="Brand does not exist.")
    
    category_brand_products = storage.filter_products(
        page_size, page_num,
        brand_id=brand_id,
        category_id=category_id
    )
    if not category_brand_products:
        abort(404, description="No category and brand found for this product.")

    category_brand_products_list = [
        get_product_dict(product) for product in category_brand_products
    ]
    return jsonify(category_brand_products_list), 200
