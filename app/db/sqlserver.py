from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings
from app.utils.test_sqlserver_db_connection import test_connection

settings = Settings()
engine_sqlserver = create_engine(settings.au_sql_server_url)

# verify connection
test_connection(engine_sqlserver)

SessionLocalSQLServer = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_sqlserver
)


def get_sqlserver_db():
    db = SessionLocalSQLServer()
    try:
        yield db
    finally:
        db.close()
