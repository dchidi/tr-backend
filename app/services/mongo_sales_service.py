from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError
from typing import List
from app.schemas.mongodb.SalesMongoSchema import SalesSchema
from app.db.mongodb import get_mongo_db
import calendar
from app.utils.previous_year_day import calculate_dates

class MongoSalesService:
    @classmethod
    async def insert_sales(cls, items: List[SalesSchema]) -> dict:
        db = await get_mongo_db()  # Retrieve the database client
        collection = db.Sales
        
        try:
            # Insert items into the collection
            result = await collection.insert_many([item.dict() for item in items])
            # Return success message with the count of inserted documents
            return {"msg": "Sales inserted successfully.", "count": len(result.inserted_ids)}
        
        except ServerSelectionTimeoutError as e:
            # Handle MongoDB server connection errors
            raise HTTPException(status_code=500, detail=f"Failed to connect to MongoDB: {e}")
        except Exception as e:
            # Handle other exceptions
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    @classmethod
    async def cummulative_sales(cls, curr_year_data: List[dict], prev_year_data:List[dict],  date_obj:datetime):
        # get total days in the month
        year = date_obj.year
        month = date_obj.month
        total_days = calendar.monthrange(year, month)[1]
        
        # generate a list of dates in the month
        first_day = date_obj.replace(day=1)
        dates = [first_day + timedelta(days=x) for x in range(total_days)]
        # print(dates)

        # get date equivalent for last year
        first_day_prev_year = calculate_dates(first_day)
        
        # generate list of dates for last year equal to the total days in the month
        first_day_prev_year = datetime.fromisoformat(first_day_prev_year).date()  # Convert string to date
        dates_prev_year = [first_day_prev_year + timedelta(days=x) for x in range(total_days)]
        # print(dates_prev_year)
        
       
        curr_year_result = []
        total_sales = 0            
        for _date in dates:
            matched = False
            if not curr_year_data: break
            for sales in curr_year_data:
                # Unpack the single key-value pair from the dictionary
                created_at, sales_count = next(iter(sales.items()))
                formatted_date = datetime.fromisoformat(created_at).date()
                
                # print(formatted_date,_date,sales, formatted_date == _date)
                if  formatted_date == _date:
                    total_sales += int(sales_count)
                    curr_year_result.append(total_sales)
                    curr_year_data.remove(sales)
                    matched = True
                    break
            if not matched:
                curr_year_result.append(total_sales)
        

        prev_year_result = []
        total_sales = 0
        for _date in dates_prev_year:
            matched = False
            if not prev_year_data: break
            for sales in prev_year_data:
                # Unpack the single key-value pair from the dictionary
                created_at, sales_count = next(iter(sales.items()))
                formatted_date = datetime.fromisoformat(created_at).date()
                
                # print(formatted_date,_date,sales, formatted_date == _date)
                if  formatted_date == _date:
                    total_sales += int(sales_count)
                    prev_year_result.append(total_sales)

                    prev_year_data.remove(sales)
                    matched = True
                    break
            if not matched:
                prev_year_result.append(total_sales)
            
        # Format the response with the year as the key
        current_year_key = date_obj.year
        prev_year_key = current_year_key - 1
 

        # print(curr_year_result, prev_year_result)

        return {str(current_year_key):curr_year_result,  str(prev_year_key):prev_year_result, "days_in_month":total_days,
                "curr_year":current_year_key, "prev_year":prev_year_key}

    @classmethod
    async def sales_by_channel(cls, data: List[dict]):
        channel ={
            "Phone": 0,
            "Web": 0,
        }
        for item in data:
            channel[item['receivedMethod']] += int(item['sales_count'])
        return channel
