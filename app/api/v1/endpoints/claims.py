from datetime import datetime, timedelta, date
from app.services.mongo_sales_service import MongoSalesService
from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List
from app.schemas.mongodb.SalesMongoSchema import SalesResponseSchema
from app.db.mongodb import get_mongo_db
from app.utils.previous_year_day import calculate_dates

router = APIRouter()

@router.get("/test")
async def test(
    start_date: date = Query(..., description="Start date for filtering results"),
    ):

    curr_data = [
        {
            "2024-09-01": 5
        },
        {
            "2024-09-02": 20
        },
        {
            "2024-09-03": 32
        },
        {
            "2024-09-04": 18
        },
        {
            "2024-09-05": 25
        },
        {
            "2024-09-06": 16
        },
        {
            "2024-09-07": 1
        },
        {
            "2024-09-08": 2
        },
        {
            "2024-09-09": 32
        },
        {
            "2024-09-10": 18
        },
        {
            "2024-09-11": 26
        },
        {
            "2024-09-12": 13
        }
    ]
    
    prev_data = [
        {
            "2023-09-04": 5
        },
        {
            "2023-09-05": 6
        },
        {
            "2023-09-06": 3
        },
        {
            "2023-09-07": 6
        },
        {
            "2023-09-08": 4
        },
        {
            "2023-09-11": 3
        },
        {
            "2023-09-12": 4
        },
        {
            "2023-09-13": 5
        },
        {
            "2023-09-14": 7
        }
    ]
    
    result = await MongoSalesService.cummulative_sales(curr_data, prev_data, start_date)
    return result
