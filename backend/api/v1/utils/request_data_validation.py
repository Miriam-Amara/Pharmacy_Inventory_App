#!/usr/bin/env python3

"""
Defines Pydantic models, enums, and validation
utilities for request data.
"""

from datetime import datetime
from enum import Enum
from flask import abort, request
from json import JSONDecodeError
from pydantic import (
    BaseModel,
    ValidationError,
    EmailStr,
    StringConstraints,
    StrictBool,
    PositiveFloat,
    PositiveInt,
    PastDatetime,
    field_validator,
)
from typing import Any, Annotated, Type, TypeVar, Optional, Tuple
import logging


T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger(__name__)


class EmployeeRole(str, Enum):
    """
    Employee roles
    """

    salesperson = "salesperson"
    manager = "manager"


class PurchaseOrderStatus(str, Enum):
    """
    Purchase order statuses.
    """

    pending = "pending"
    in_progress = "in progress"
    complete = "complete"
    cancelled = "cancelled"

class SaleOrderStatus(str, Enum):
    """Represents the current stage of a sale order."""

    pending = "pending"
    complete = "complete"


class ItemStatus(str, Enum):
    """
    Purchase or Sale statuses.
    """

    pending = "pending"
    supplied = "supplied"
    cancelled = "cancelled"


class PaymentStatus(str, Enum):
    """
    Payment statuses.
    """

    paid = "paid"
    unpaid = "unpaid"
    partial_payment = "partial payment"

class SalesPaymentStatus(str, Enum):
    """
    Payment statuses.
    """

    paid = "paid"
    unpaid = "unpaid"

class EmployeeLogin(BaseModel):
    """
    Schema for employee login validation.
    """
    email_or_username: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        )
    ]
    password: Annotated[
        str,
        StringConstraints(
            min_length=8,
            max_length=200,
            strip_whitespace=True
        )
    ]


class EmployeeRegister(BaseModel):
    """
    Schema for employee registration validation.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    first_name: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    middle_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=3,
                max_length=200,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    last_name: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    username: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    email: EmailStr
    password: Annotated[
        str,
        StringConstraints(
            min_length=8,
            max_length=200,
            strip_whitespace=True
        )
    ]
    home_address: Annotated[
        str,
        StringConstraints(
            min_length=10,
            max_length=500,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    role: EmployeeRole
    file_name: Optional[Annotated[
        str,
        StringConstraints(
            pattern=r'^[a-zA-Z0-9_\-]+\.(jpg|jpeg|png)$',
            max_length=100
        )
    ]] = None
    is_admin: Optional[StrictBool] = None

    @field_validator("email", "role", mode="before")
    @classmethod
    def lowercase_email_username(cls, v: str) -> str:
        """
        Convert email and role to lowercase.
        """
        return v.lower()

    @field_validator("password")
    @classmethod
    def check_complexity(cls, v: str):
        """
        Ensure password contains uppercase and digit.
        """
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain an uppercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain a digit")
        return v


class EmployeeUpdate(BaseModel):
    """
    Schema for updating employee details.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    first_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=3,
                max_length=200,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    middle_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=3,
                max_length=200,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    last_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=3,
                max_length=200,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    home_address: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=10,
                max_length=500,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    role: Optional[EmployeeRole] = None
    file_name: Optional[Annotated[
        str,
        StringConstraints(
            pattern=r'^[a-zA-Z0-9_\-]+\.(jpg|jpeg|png)$',
            max_length=100
        )
    ]] = None
    is_admin: Optional[StrictBool] = None


class BrandRegister(BaseModel):
    """
    Schema for brand creation.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    name: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    is_active: Optional[StrictBool] = True


class BrandUpdate(BaseModel):
    """
    Schema for updating brand details.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=3,
                max_length=200,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    is_active: Optional[StrictBool] = True


class CategoryRegister(BaseModel):
    """
    Schema for category creation.
    """

    name: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    description: Optional[Annotated[
        str,
        StringConstraints(
            max_length=2000,
            to_lower=True,
            strip_whitespace=True
        ),
    ]] = None


class CategoryUpdate(BaseModel):
    """
    Schema for updating category details.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=3,
                max_length=200,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    description: Optional[
        Annotated[
            str,
            StringConstraints(
                max_length=2000,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None


class ProductRegister(BaseModel):
    """
    Schema for product creation.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    barcode: Optional[Annotated[str, StringConstraints(max_length=20)]] = None
    name: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    category_id: Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    brand_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            to_lower=True,
            strip_whitespace=True
        ),
    ]] = None
    brand_name: Optional[Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        ),
    ]] = None
    unit_cost_price: Annotated[float, PositiveFloat]
    unit_selling_price: Annotated[float, PositiveFloat]
    ordering_cost: Optional[Annotated[float, PositiveFloat]] = None
    holding_cost_rate: Optional[Annotated[float, PositiveFloat]] = None
    lead_time: Optional[Annotated[int, PositiveInt]] = None


class ProductUpdate(BaseModel):
    """
    Schema for updating product details.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    barcode: Optional[Annotated[str, StringConstraints(max_length=20)]] = None
    name: Optional[Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        ),
    ]] = None
    category_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            to_lower=True,
            strip_whitespace=True
        ),
    ]] = None
    brand_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            to_lower=True,
            strip_whitespace=True
        ),
    ]] = None
    brand_name: Optional[Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        ),
    ]] = None
    unit_cost_price: Optional[Annotated[float, PositiveFloat]] = None
    unit_selling_price: Optional[Annotated[float, PositiveFloat]] = None
    ordering_cost: Optional[Annotated[float, PositiveFloat]] = None
    holding_cost_rate: Optional[Annotated[float, PositiveFloat]] = None
    lead_time: Optional[Annotated[int, PositiveInt]] = None

class PurchaseOrderRegister(BaseModel):
    """
    Schema for purchase order creation.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    supplier_name: Optional[Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        )
    ]] = None
    status: Optional[PurchaseOrderStatus] = PurchaseOrderStatus.pending
    holding_cost_rate: Optional[Annotated[float, PositiveFloat]] = None
    ordering_cost: Annotated[float, PositiveFloat]


class PurchaseOrderUpdate(BaseModel):
    """
    Schema for updating purchase order.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    supplier_name: Optional[Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200,
            to_lower=True,
            strip_whitespace=True
        )
    ]] = None
    status: Optional[PurchaseOrderStatus] = PurchaseOrderStatus.pending
    holding_cost_rate: Optional[Annotated[float, PositiveFloat]] = None
    ordering_cost: Optional[Annotated[float, PositiveFloat]] = None


class PurchaseRegister(BaseModel):
    """
    Schema for adding items to a purchase order.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    purchase_order_id: Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    product_id: Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    quantity: Annotated[int, PositiveInt]
    unit_cost_price: Annotated[float, PositiveFloat]
    total_cost_price: Annotated[float, PositiveFloat]
    payment_status: PaymentStatus
    item_status: Optional[ItemStatus] = ItemStatus.pending


class PurchaseUpdate(BaseModel):
    """
    Schema for updating purchase order items.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    purchase_order_id: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=36,
                max_length=36,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    product_id: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=36,
                max_length=36,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    quantity: Optional[Annotated[int, PositiveInt]] = None
    unit_cost_price: Optional[Annotated[float, PositiveFloat]] = None
    total_cost_price: Optional[Annotated[float, PositiveFloat]] = None
    payment_status: Optional[PaymentStatus] = None
    item_status: Optional[ItemStatus] = None


class SaleOrderRegister(BaseModel):
    """
    Schema for purchase order creation.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    status: Optional[PurchaseOrderStatus] = PurchaseOrderStatus.pending


class SaleOrderUpdate(BaseModel):
    """
    Schema for updating purchase order.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    status: Optional[PurchaseOrderStatus] = PurchaseOrderStatus.pending


class SaleRegister(BaseModel):
    """
    Schema for sales creation.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    sale_order_id: Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    product_id: Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            to_lower=True,
            strip_whitespace=True
        ),
    ]
    quantity: Annotated[int, PositiveInt]
    unit_selling_price: Annotated[float, PositiveFloat]
    total_selling_price: Annotated[float, PositiveFloat]
    payment_status: SalesPaymentStatus


class SaleUpdate(BaseModel):
    """
    Schema for updating sales records.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    sale_order_id: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=36,
                max_length=36,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    product_id: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=36,
                max_length=36,
                to_lower=True,
                strip_whitespace=True
            ),
        ]
    ] = None
    quantity: Optional[Annotated[int, PositiveInt]] = None
    unit_selling_price: Optional[Annotated[float, PositiveFloat]] = None
    total_selling_price: Optional[Annotated[float, PositiveFloat]] = None
    payment_status: Optional[SalesPaymentStatus] = None


class StockLevelUpdate(BaseModel):
    """
    Schema for editing current stock.
    """
    created_at: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    last_updated: Optional[Annotated[
        datetime,
        PastDatetime
    ]] = None
    product_id: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=36,
                max_length=36,
                strip_whitespace=True
            ),
        ]
    ] = None
    quantity_in_stock: Optional[Annotated[int, PositiveInt]] = None


def get_request_data() -> dict[str, Any]:
    """
    Extract and validate JSON from the request.
    """
    try:
        request_data: dict[str, Any] = request.get_json()
    except JSONDecodeError:
        abort(400, description="Not a json")

    return request_data


def validate_form_data(validation_cls: Type[T]) -> Tuple[dict[str, Any], Any]:
    """
    """
    form_data = request.form.to_dict()
    file = request.files.get("image")

    if not form_data and not file:
        form_data = get_request_data()

    try:
        valid_data = validation_cls(**form_data)
    except ValidationError as e:
        abort(400, description=e.errors())

    if not valid_data.model_dump(exclude_none=True) and not file:
        abort(400, description="Request data cannot be empty")
    return valid_data.model_dump(exclude_unset=True), file


def validate_request_data(validation_cls: Type[T]) -> dict[str, Any]:
    """
    Validate incoming request data against a Pydantic model.
    """
    request_data = get_request_data()

    if not issubclass(validation_cls, BaseModel):  # type: ignore
        logger.error(
            "Validation class must inherit from pydantic BaseModel"
        )
        abort(500)

    try:
        valid_data = validation_cls(**request_data)
    except ValidationError as e:
        abort(400, description=e.errors())

    if not valid_data.model_dump(exclude_none=True):
        abort(400, description="Request data cannot be empty")
    return valid_data.model_dump(exclude_unset=True)
