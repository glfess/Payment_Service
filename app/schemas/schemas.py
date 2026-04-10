from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.utils.enums import PaymentStatus, Currency

class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amount: Decimal
    currency: Currency
    description: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    status: PaymentStatus
    webhook_url: HttpUrl

    created_at: datetime
    processed_at: Optional[datetime] = None

class PaymentCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: Decimal
    currency: Currency
    description: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    webhook_url: HttpUrl

class PaymentCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    payment_id: UUID = Field(..., alias="id")
    status: PaymentStatus
    created_at: datetime