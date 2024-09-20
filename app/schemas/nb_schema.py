from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import Optional

class NBSchema(BaseModel):
    created_at: str  # Change to str to handle serialization
    country: str
    receivedMethod: str
    sales_count: float
    product: Optional[str] = None

    @validator('created_at', pre=True, always=True)
    def parse_date(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()  # Convert datetime to ISO 8601 format
        if isinstance(v, date):
            return datetime.combine(v, datetime.min.time()).isoformat()  # Convert date to datetime and then to ISO 8601
        return v
