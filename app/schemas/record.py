from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SalesRecordBase(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=150)
    category: str = Field(..., min_length=2, max_length=100)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    customer_name: str = Field(..., min_length=2, max_length=150)
    region: str = Field(..., min_length=2, max_length=100)


class SalesRecordCreate(SalesRecordBase):
    pass


class SalesRecordResponse(SalesRecordBase):
    id: int
    created_at: datetime
    total_amount: float

    model_config = ConfigDict(from_attributes=True)
