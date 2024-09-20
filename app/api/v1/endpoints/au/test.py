from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.au.db_connect import get_au_uts_session

router = APIRouter()


@router.get("/items/")
def read_items(session: Session = Depends(get_au_uts_session)):
    # Execute the raw SQL query using text()
    query = text("SELECT TOP 2 * FROM Policy")
    result = session.execute(query)

    # Convert each row to a dictionary using row._mapping
    items = [dict(row._mapping) for row in result.fetchall()]
    return items
