# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime

# class SalesBase(BaseModel):
#     UrlCode: Optional[str]
#     AccountTypeId: Optional[int]
#     Name: Optional[str]
#     Description: Optional[str]
#     CreatedBy: Optional[str]
#     CreatedDate: Optional[datetime]
#     UpdatedBy: Optional[str]
#     UpdatedDate: Optional[datetime]

#     class Config:
#         from_attributes = True
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

BaseSQLServer = declarative_base()

class Sales(BaseSQLServer):
    __tablename__ = "Account"  # This should be the name of your table
    __table_args__ = {"schema": "dbo"}  # Specify the schema if necessary

    Id = Column(Integer, primary_key=True, index=True)
    UrlCode = Column(String)
    AccountTypeId = Column(Integer)
    Name = Column(String)  
    Description = Column(String)
    CreatedBy = Column(String)
    CreatedDate = Column(DateTime)
    UpdatedBy = Column(String)
    UpdatedDate = Column(DateTime)
