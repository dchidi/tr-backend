from app.models.sales import Sales
from app.schemas.sales_schema import SalesSchema
from app.db.sqlserver import get_sqlserver_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/account", response_model=List[SalesSchema])
def get_account(db: Session = Depends(get_sqlserver_db)):
    try:
        # Fetch the top 10 records from the Account table
        accounts = db.query(Sales).limit(10).all()
        return accounts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
