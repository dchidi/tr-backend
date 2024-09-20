from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

BaseSQLServer = declarative_base()

class Account(BaseSQLServer):
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
