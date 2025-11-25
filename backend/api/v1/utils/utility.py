#!/usr/bin/env python3

"""
Utility functions and database helpers.
"""

# from datetime import datetime, timedelta
from werkzeug.datastructures import FileStorage
from flask import abort, current_app
from io import BytesIO
from PIL import Image
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from typing import Type, TypeVar, Any
from uuid import uuid4
# import calendar
import logging
import magic
import os

from models import storage
from models.basemodel import BaseModel
from models.employee import Employee
# from models.stock_level import ReorderingPoint

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


def check_email_username_exists(data: dict[str, Any]) -> None:
    """
    """
    if "email" in data:
        employee = Employee.search_employee_by_email_username(
            data["email"]
        )
        if employee:
            abort(409, description="Email already exist.")

    if "username" in data:
        employee = Employee.search_employee_by_email_username(
            data["username"]
        )
        if employee:
            abort(409, description="Username already exists.")


def get_obj(cls: Type[T], id: str) -> T | None:
    """
    Fetch a record by ID.
    """

    if not issubclass(cls, BaseModel):  # type: ignore
        abort(400, description="Invalid class")
    if not isinstance(id, str):  # type: ignore
        abort(400, description="id must be a valid string.")

    obj = storage.get_obj_by_id(cls, id)
    return obj


# def run_monthly_reordering_point_update():
#     """
#     """
#     # Calculate last month
#     today = datetime.today()
#     first_day_this_month = datetime(today.year, today.month, 1)
#     last_month_date = first_day_this_month - timedelta(days=1)
#     year = last_month_date.year
#     month = last_month_date.month
#     days_in_month: int = calendar.monthrange(year, month)[1]

#     all_products = storage.all_products()
#     if not all_products:
#         abort(404, description="No product found")

#     for product in all_products:
#         for brand in product.brands:
#             monthly_summary = storage.get_monthly_sales_summary(
#                 product.id, brand.id, year, month
#             )
#             if not monthly_summary or not monthly_summary["total_quantity"]:
#                 total_monthly_demand = 0
#             else:
#                 total_monthly_demand = monthly_summary["total_quantity"]
            
#             lead_time = storage.get_lead_time(product.id, brand.id)
#             if not lead_time:
#                 lead_time = 0

#             ave_monthly_demand = total_monthly_demand / days_in_month
#             safety_stock = 0.02 * (ave_monthly_demand * lead_time)

#             reordering_point = (ave_monthly_demand * lead_time) + safety_stock

#             prev_reordering_point = storage.get_last_month_reordering_point(
#                 brand.id, product.id
#             )

#             significant_increase = prev_reordering_point + (0.02 * prev_reordering_point)
#             if reordering_point >= significant_increase:
#                 new_reordering_point = reordering_point
#                 rop = ReorderingPoint(**{
#                     "product_id": product.id, 
#                     "brand_id": brand.id,
#                     "reordering_point": new_reordering_point,
#                     }
#                 )
#                 rop.save()


class DatabaseOp:
    """
    imple wrapper for database operations.
    """

    def save(self, obj: BaseModel):
        """
        Save object to database.
        """
        try:
            obj.save()
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                detail = e.orig.diag.message_detail
                if detail:
                    detail = detail.replace("Key ", "")
                abort(409, description=detail)
            else:
                logger.error(f"Database operation failed: {e}")
                abort(500)
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            abort(500)

    def commit(self):
        """
        Commit all changes.
        """
        try:
            storage.save()
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            abort(500)

    def delete(self, obj: BaseModel):
        """
        Delete object from database.
        """
        try:
            obj.delete()
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            abort(500)


class FileManager:
    """
    """
    max_image_size = 1 * 1024 * 1024

    def allowed_mime(self, mime_type: str) -> bool:
        return mime_type in ('image/jpeg', 'image/jpg', 'image/png')

    def compress_image(self, image: Image.Image) -> BytesIO:
        """
        Resize an compress images.
        Steps:
        1. Remove EXIF metadata
        2. Convert to RGB
        3. Resize if image is larger than max dimension
        4. Save as JPEG with decreasing quality
        """
        max_dimension = 800

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        else:
            image = image.copy()
        
        width, height = image.size
        if max(width, height) > max_dimension:
            image.thumbnail((max_dimension, max_dimension))
        
        img_bytes = BytesIO()
        quality = 85
        
        while True:
            img_bytes.seek(0)
            img_bytes.truncate(0)
            
            image.save(img_bytes, format="JPEG", optimize=True, quality=quality)

            if img_bytes.tell() <= self.max_image_size or quality <= 40:
                break

            quality -= 5
        
        img_bytes.seek(0)

        return img_bytes

    def validate_request(self, file: FileStorage) -> FileStorage:
        """
        Verifies file is uploaded and has file name
        """
        if not isinstance(file, FileStorage): # type: ignore
            abort(400, description="Invalid file")

        if not file.filename or not file.filename.strip():
            abort(400, description="No file name")

        return file
    
    def validate_file(self, file_bytes: bytes) -> str:
        """
        Verifies file mime type and ensure file is not corrupt.
        """
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(file_bytes)
        if not self.allowed_mime(mime_type):
            abort(
                400,
                description=f"Invalid file format {mime_type}."
                " Allowed files are: jpeg, jpg, png"
            )

        try:
            image = Image.open(BytesIO(file_bytes))
            image.verify()  # Validate image is not corrupt
        except Exception:
            abort(
                400,
                description="Uploaded file is not a valid image."
            )
        return mime_type
    
    def validate_file_size(self, file_bytes: bytes, mime_type: str) -> BytesIO:
        """
        """
        image = Image.open(BytesIO(file_bytes))

        if len(file_bytes) <= self.max_image_size:
            return BytesIO(file_bytes)
        
        if mime_type in ["image/jpeg", "image/jpg"]:
            compressed = self.compress_image(image)

            if compressed.getbuffer().nbytes > self.max_image_size:
                abort(400, description="Image too large even after compression.")
            return compressed
        
        abort(
            400,
            description="Maximum image size exceeded"
            f" {self.max_image_size/(1024*1024)}mb."
        )

    def upload_file(
            self, img_bytes: BytesIO, ext: str,
            image_type: str, obj: BaseModel | None=None
        ) -> str:
        """
        """
        folder = {
            "employee": "employees_images",
            "products": "products_images",
        }.get(image_type, "other")

        static_folder = os.path.join("static", folder)
        os.makedirs(static_folder, exist_ok=True)

        image_filepath = getattr(obj, "image_filepath", None) if obj else None

        if image_filepath:
            absolute_path = os.path.abspath(image_filepath)

            if os.path.exists(absolute_path):
                os.remove(absolute_path)

        filename = f"{uuid4().hex}.{ext}"
        project_root = os.path.abspath(os.path.join(current_app.root_path, "..", ".."))
        filepath = os.path.join(project_root, "static", folder, filename)

        img_bytes.seek(0)
        with open(filepath, "wb") as f:
            f.write(img_bytes.read())

        return filepath

    def process_file(
            self, file: FileStorage, image_type: str, obj: BaseModel | None=None
        ) -> str:
        """
        """
        file = self.validate_request(file)
        file_bytes = file.read()

        mime_type = self.validate_file(file_bytes)
        img_bytes = self.validate_file_size(file_bytes, mime_type)

        ext = "jpg" if mime_type == "image/jpeg" else "png"

        if obj:
            image_filepath = self.upload_file(img_bytes, ext, image_type, obj)
        else:
            image_filepath = self.upload_file(img_bytes, ext, image_type)

        return image_filepath 
