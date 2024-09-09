from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def test_connection(engine):
    try:
        # Test the connection by executing a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() == 1:
                print("Database connection successful!")
            else:
                print("Database connection failed: Unexpected result.")
    except SQLAlchemyError as e:
        print(f"Database connection failed: {e}")
        raise