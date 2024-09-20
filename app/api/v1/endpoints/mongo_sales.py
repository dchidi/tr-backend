from fastapi import APIRouter, Query, HTTPException,HTTPException, File, UploadFile
from typing import Dict, List
from datetime import date, timedelta
from app.schemas.mongodb.SalesMongoSchema import SalesResponseSchema
from app.db.mongodb import get_mongo_db
from app.utils.previous_year_day import calculate_dates
from app.services.mongo_sales_service import MongoSalesService
import calendar
import pandas as pd
import io

router = APIRouter()

# Query Fixed on AU for now

async def fetch_sales_data(collection, start_datetime, end_datetime):
    pipeline = [
        {
            "$match": {
                "created_at": {
                    "$gte": start_datetime,
                    "$lt": end_datetime
                },
                "country":"AU"
            }
        },
        {
            "$project": {
                "date": {"$substr": ["$created_at", 0, 10]},  # Extract date part from ISO string
                "sales_count": 1  # Keep the sales_count field
            }
        },
        {
            "$group": {
                "_id": "$date",  # Group by the extracted date
                "total_sales": {"$sum": "$sales_count"}  # Sum the sales_count field
            }
        },
        {
            "$sort": {"_id": 1}  # Sort by date in ascending order
        }
    ]
    
    cursor = collection.aggregate(pipeline)
    return [{item['_id']: item['total_sales']} for item in await cursor.to_list(length=None)]
    
async def fet_sales_by_channel(collection, from_date, to_date):
    query = {
            "created_at": {
                "$gte": from_date,
                "$lt": to_date
            },
            "country" : "AU"
        }
    cursor = collection.find(query)
    # Convert cursor to list
    sales_data = await cursor.to_list(length=None)
    return sales_data

def percentage_diff(a, b):
    if b == 0:
        return 0
    return round(((a - b) / b) * 100, 1)

def percentage_tgt_diff(a, b):
    if a == 0:
        return 0
    return round(((b - a) / a) * 100, 1)

def get_month_bounds_last_year(start_date):
    try:
        last_year_date = start_date.replace(year=start_date.year - 1)
    except ValueError:
        # Handles February 29 by setting to February 28
        last_year_date = start_date.replace(year=start_date.year - 1, day=28)
    first_day = last_year_date.replace(day=1)
    last_day_num = calendar.monthrange(last_year_date.year, last_year_date.month)[1]
    last_day = last_year_date.replace(day=last_day_num)
    return first_day, last_day
         

@router.get("/report_sales")
async def get_graph_data(
    start_date: date = Query(..., description="Start date for filtering results"),
    end_date: date = Query(..., description="End date for filtering results. End date is not included in the result set")
) :
    db = await get_mongo_db()
    collection = db.Sales

    # Convert start_date and end_date to ISO 8601 strings for MongoDB queries
    _end_date = end_date + timedelta(days=1)   # Include end_date in the result set
    start_datetime = start_date.isoformat()
    end_datetime = _end_date.isoformat()

    # Get previous year records
    last_year_start = calculate_dates(start_date)
    last_year_end = calculate_dates(_end_date)

    try:
        # Fetch aggregated sales data for the current year and previous year
        current_year_sales = await fetch_sales_data(collection, start_datetime, end_datetime)
        prev_year_sales = await fetch_sales_data(collection, last_year_start, last_year_end)

        # Format the response with the year as the key
        # current_year_key = start_date.year
        # prev_year_key = current_year_key - 1

        graph_data = await MongoSalesService.cummulative_sales(current_year_sales, prev_year_sales, start_date)

        return graph_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.get("/report_sales_table_data")
async def get_table_data(
    start_date: date = Query(..., description="Start date for filtering results"),
    end_date: date = Query(..., description="End date for filtering results. End date is not included in the result set")
) :
    db = await get_mongo_db()
    collection = db.Sales

    # Convert start_date and end_date to ISO 8601 strings for MongoDB queries    
    start_datetime = start_date.isoformat()
    end_datetime = end_date.isoformat()
    _end_date = end_date + timedelta(days=1)   # Include end_date in the result set

    # Get previous year records
    last_year_start = calculate_dates(start_date)
    last_year_end = calculate_dates(_end_date)

    headers = [
        {"label":"label", "value":"All Geos Data"},
        {"label":"current_sales", "value":"NB"},
        {"label":"curr_year_mtd", "value":"MTD"},
        {"label":"prev_year_mtd", "value":f"MTD {start_date.strftime('%b')} {start_date.year - 1}"},
        {"label":"diff_mtd", "value":"Difference (MTD) #"},
        {"label":"diff_mtd_percent", "value":"Difference (MTD) %"},
        {"label":"total_month_prev_year", "value":f"{start_date.strftime('%b')} {start_date.year - 1} Total"},
        {"label":"target_mtd", "value":"MTD Target"},
        {"label":"target_diff", "value":"Target Difference (Target x MTD)"},
        {"label":"target_diff_percent", "value":"Target Delta (MTD) %"}
        ]
    phone_sales ={"label":"Contact Center", "current_sales":0,"curr_year_mtd":0,"prev_year_mtd":0,
                  "diff_mtd":0, "diff_mtd_percent":0, "total_month_prev_year":0, "target_mtd":0, "target_diff":0, 
                  "target_diff_percent":0}

    web_sales ={"label":"Web", "current_sales":0,"curr_year_mtd":0,"prev_year_mtd":0,
                  "diff_mtd":0, "diff_mtd_percent":0, "total_month_prev_year":0, "target_mtd":0, "target_diff":0, 
                  "target_diff_percent":0}

    total_sales ={"label":"Total", "current_sales":0,"curr_year_mtd":0,"prev_year_mtd":0,
                  "diff_mtd":0, "diff_mtd_percent":0, "total_month_prev_year":0, "target_mtd":0, "target_diff":0, 
                  "target_diff_percent":0}

    try:
       
        sales_data = await fet_sales_by_channel(collection, from_date= end_datetime ,to_date= _end_date.isoformat())
        nb_current_year = await MongoSalesService.sales_by_channel(sales_data)

        curr_year_mtd = await fet_sales_by_channel(collection, from_date= start_datetime ,to_date= _end_date.isoformat())
        nb_curr_year_mtd = await MongoSalesService.sales_by_channel(curr_year_mtd)

        prev_year_mtd = await fet_sales_by_channel(collection, from_date= last_year_start ,to_date= last_year_end)
        nb_prev_year_mtd = await MongoSalesService.sales_by_channel(prev_year_mtd)

        # Total month data for previous year
        first_day_of_month_prev_year , last_day_of_month_prev_year= get_month_bounds_last_year(start_date)

        prev_year_total_month = await fet_sales_by_channel(collection, from_date= first_day_of_month_prev_year.isoformat(), 
                                                           to_date= last_day_of_month_prev_year.isoformat())
        
        total_month_prev_year = await MongoSalesService.sales_by_channel(prev_year_total_month)

        # New business for end date selected
        phone_sales["current_sales"]= nb_current_year["Phone"]
        web_sales["current_sales"]= nb_current_year["Web"]
        total_sales["current_sales"]= phone_sales["current_sales"] +  web_sales["current_sales"]


        # New business MTD current year
        phone_sales["curr_year_mtd"]= nb_curr_year_mtd["Phone"]
        web_sales["curr_year_mtd"]= nb_curr_year_mtd["Web"]
        total_sales["curr_year_mtd"]= phone_sales["curr_year_mtd"] +  web_sales["curr_year_mtd"]

        # New business MTD prev year
        phone_sales["prev_year_mtd"]= nb_prev_year_mtd["Phone"]
        web_sales["prev_year_mtd"]= nb_prev_year_mtd["Web"]
        total_sales["prev_year_mtd"]= phone_sales["prev_year_mtd"] +  web_sales["prev_year_mtd"]

        # Difference MTD
        phone_sales["diff_mtd"]= phone_sales["curr_year_mtd"] - phone_sales["prev_year_mtd"]
        web_sales["diff_mtd"]= web_sales["curr_year_mtd"] - web_sales["prev_year_mtd"]
        total_sales["diff_mtd"]= phone_sales["diff_mtd"] +  web_sales["diff_mtd"]
        
        # Percentage Difference MTD   
        phone_sales["diff_mtd_percent"]= percentage_diff(phone_sales["curr_year_mtd"], phone_sales["prev_year_mtd"])
        web_sales["diff_mtd_percent"]= percentage_diff(web_sales["curr_year_mtd"], web_sales["prev_year_mtd"])
        total_sales["diff_mtd_percent"]= percentage_diff(total_sales["curr_year_mtd"], total_sales["prev_year_mtd"])

        # Total month value for prev year
        phone_sales["total_month_prev_year"]= total_month_prev_year["Phone"] 
        web_sales["total_month_prev_year"]= total_month_prev_year["Web"] 
        total_sales["total_month_prev_year"]= phone_sales["total_month_prev_year"] +  web_sales["total_month_prev_year"]
        
        # MTD Target current year
        phone_sales["target_mtd"]= round(phone_sales["prev_year_mtd"] * 1.15, 1) # 15% + total  mtd prev year
        web_sales["target_mtd"]= round(web_sales["prev_year_mtd"] * 1.15, 1)
        total_sales["target_mtd"]= round(total_sales["prev_year_mtd"] * 1.15, 1)

        # MTD Target Difference
        phone_sales["target_diff"]= round(phone_sales["target_mtd"] - phone_sales["curr_year_mtd"],0)
        web_sales["target_diff"]= round(web_sales["target_mtd"] - web_sales["curr_year_mtd"],0)
        total_sales["target_diff"]= round(phone_sales["target_diff"] +  web_sales["target_diff"],0)

        # MTD Target Difference Percentage
        phone_sales["target_diff_percent"]= percentage_tgt_diff(phone_sales["target_mtd"], phone_sales["curr_year_mtd"])
        web_sales["target_diff_percent"]= percentage_tgt_diff(web_sales["target_mtd"], web_sales["curr_year_mtd"])
        total_sales["target_diff_percent"]= percentage_tgt_diff(total_sales["target_mtd"], total_sales["target_mtd"])

        return {"phone":phone_sales, "web":web_sales, "headers":headers, "total":total_sales}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    db = await get_mongo_db()
    collection = db.Sales
    """Endpoint to upload CSV and insert data into MongoDB."""
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")

    try:
        # Read the uploaded file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        # Convert DataFrame to dictionary records
        records = df.to_dict('records')

        # Insert records into MongoDB
        if records:
            result = await collection.insert_many(records)
            return {'message': 'File successfully uploaded and data inserted into MongoDB'}
        else:
            raise HTTPException(status_code=400, detail="CSV file is empty")
    except Exception as e:
        # Handle exceptions (e.g., parsing errors, database errors)
        raise HTTPException(status_code=500, detail=str(e))