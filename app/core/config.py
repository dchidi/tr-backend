from pydantic_settings import BaseSettings


import os


class Settings(BaseSettings):
    environment:str

    app_name: str = "Trade Report Platform"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Email settings
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    email_from: str

    # AU DB Connection
    au_sql_server_host: str
    au_sql_server_user: str
    au_sql_server_password: str
    au_sql_server_db: str

    # Mongo DB
    mongo_url:str
    
    
    # Automatically load .env file content into environment variable.
    class Config:
        env_file = ".env"
    
    @property
    def au_sql_server_url(self) -> str:
        # "mssql+pymssql://username:password@localhost/sales_database"
        return f"mssql+pymssql://{self.au_sql_server_user}:{self.au_sql_server_password}@{self.au_sql_server_host}/{self.au_sql_server_db}"


# class DevelopmentSettings(Settings):
#     mongo_url: str = os.getenv("DEV_MONGO_URL")


# class ProductionSettings(Settings):
#     mongo_url: str = os.getenv("PRODUCTION_MONGO_URL")


# Dynamically load the appropriate settings based on the environment
# environment = os.getenv("ENVIRONMENT", "development")

# if environment == "production":
#     settings = ProductionSettings()
# else:
#     settings = DevelopmentSettings()
settings =Settings()
