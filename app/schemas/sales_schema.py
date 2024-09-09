from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SalesSchema(BaseModel):
    Id: int
    UrlCode: Optional[str]
    AccountTypeId: Optional[int]
    Name: Optional[str]
    Description: Optional[str]
    CreatedBy: Optional[str]
    CreatedDate: Optional[datetime]
    UpdatedBy: Optional[str]
    UpdatedDate: Optional[datetime]

    class Config:
        from_attributes = True
