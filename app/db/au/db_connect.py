from sqlalchemy.orm import Session
from app.core.config import Settings
from app.db.base_connection import SQLServerConnection
from typing import Generator

# Load settings
settings = Settings()

# Initialize SQL Server connections
au_uts = SQLServerConnection(settings.sql_server_uts_url_au)
au_fit = SQLServerConnection(settings.sql_server_fit_url_au)


def get_au_uts_session() -> Generator[Session, None, None]:
    """
    Provides a session for the AU UTS database.
    """
    yield from au_uts.get_session()


def get_au_fit_session() -> Generator[Session, None, None]:
    """
    Provides a session for the AU FIT database.
    """
    yield from au_fit.get_session()
