from app.models.account import Account
from app.schemas.sales_schema import SalesSchema
from app.db.sqlserver import get_au_fit_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/account", response_model=List[SalesSchema])
def get_account(db: Session = Depends(get_au_fit_session)):
    try:
        # Fetch the top 10 records from the Account table
        accounts = db.query(Account).limit(10).all()
        return accounts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
