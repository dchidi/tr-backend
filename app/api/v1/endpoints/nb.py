from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from datetime import date
from app.schemas.nb_schema import NBSchema
from app.schemas.insert_schema import InsertResponseSchema
from app.db.sqlserver import get_au_fit_session, get_au_uts_session
from app.db.sql_server_queries.nb_query import nb_fit_query, nb_uts_query
from app.utils.previous_year_day import calculate_dates
from app.services.mongo_sales_service import MongoSalesService

router = APIRouter()

def execute_query(db: Session, query: str, start_date: date, end_date: date) -> List[NBSchema]:
    try:
        # Define the raw SQL query with a placeholder for the date and Execute it
        sql_query = text(query)
        result = db.execute(sql_query, {"start_date": start_date,"end_date": end_date})
        
        # Convert the result into a list of dictionaries
        rows = result.mappings().all()
        
        # Return the results mapped to the SalesSchema
        return [NBSchema(**row) for row in rows]    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nb_au_fit", response_model=InsertResponseSchema)
async def get_nb_au_fit(
    db: Session = Depends(get_au_fit_session),
    start_date: date = Query(..., description="Start date for filtering result"),
    end_date: date = Query(..., description="End date for filtering result. End date is not included in the result set")
):
    data = execute_query(db, nb_fit_query, start_date, end_date)    
    # result = await MongoSalesService.insert_sales(data)
    # return result
  
    if data:
        result = await MongoSalesService.insert_sales(data)
    else: 
        result = {"msg": "No sales record", "count": 0}
    return result

@router.get("/nb_au_uts", response_model=InsertResponseSchema)
async def get_nb_au_uts(
    db: Session = Depends(get_au_uts_session),
    start_date: date = Query(..., description="Start date for filtering result"),
    end_date: date = Query(..., description="End date for filtering result. End date is not included in the result set")
):
    data = execute_query(db, nb_uts_query, start_date, end_date)
        
    if data:
        result = await MongoSalesService.insert_sales(data)
    else: 
        result = {"msg": "No sales record", "count": 0}
    return result

# @router.get("/nb_au_fit_last_year", response_model=List[NBSchema])
# async def get_nb_au_fit(
#     db: Session = Depends(get_au_fit_session),
#     start_date: date = Query(..., description="Start date for filtering result"),
#     end_date: date = Query(..., description="End date for filtering result. End date is not included in the result set")
# ):
#     last_year_start_date = calculate_dates(start_date)
#     last_year_end_date = calculate_dates(end_date)
#     return execute_query(db, nb_fit_query, last_year_start_date, last_year_end_date)

# @router.get("/nb_au_uts_last_year", response_model=List[NBSchema])
# async def get_nb_au_uts(
#     db: Session = Depends(get_au_uts_session),
#     start_date: date = Query(..., description="Start date for filtering result"),
#     end_date: date = Query(..., description="End date for filtering result. End date is not included in the result set")
# ):
#     last_year_start_date = calculate_dates(start_date)
#     last_year_end_date = calculate_dates(end_date)
#     return execute_query(db, nb_uts_query, last_year_start_date, last_year_end_date)