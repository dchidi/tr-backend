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

    # AU uts connection credentials
    au_uts_host: str
    au_uts_user: str
    au_uts_password: str
    au_uts_db_name: str

    # AU fit connection credentials
    au_fit_host: str
    au_fit_user: str
    au_fit_password: str
    au_fit_db_name: str

    # NZ uts connection credentials
    nz_uts_host: str
    nz_uts_user: str
    nz_uts_password: str
    nz_uts_db_name: str

    # NZ fit connection credentials
    nz_fit_host: str
    nz_fit_user: str
    nz_fit_password: str
    nz_fit_db_name: str

    # UK, AT and DE uts connection credentials
    uk_at_de_uts_host: str
    uk_at_de_uts_user: str
    uk_at_de_uts_password: str
    uk_uts_db_name: str
    at_uts_db_name: str
    de_uts_db_name: str

    # Mongo DB
    mongo_url:str
    
    
    # Automatically load .env file content into environment variable.
    class Config:
        env_file = ".env"
    
    @property
    def sql_server_uts_url_au(self) -> str:
        # "mssql+pymssql://username:password@localhost/sales_database"
        return f"mssql+pymssql://{self.au_uts_user}:{self.au_uts_password}@{self.au_uts_host}/{self.au_uts_db_name}"
    
    @property
    def sql_server_fit_url_au(self) -> str:
        # "mssql+pymssql://username:password@localhost/sales_database"
        return f"mssql+pymssql://{self.au_fit_user}:{self.au_fit_password}@{self.au_fit_host}/{self.au_fit_db_name}"
    
    @property
    def sql_server_uts_url_nz(self) -> str:
        # "mssql+pymssql://username:password@localhost/sales_database"
        return f"mssql+pymssql://{self.nz_uts_user}:{self.nz_uts_password}@{self.nz_uts_host}/{self.nz_uts_db_name}"
    
    @property
    def sql_server_fit_url_nz(self) -> str:
        # "mssql+pymssql://username:password@localhost/sales_database"
        return f"mssql+pymssql://{self.nz_fit_user}:{self.nz_fit_password}@{self.nz_fit_host}/{self.nz_fit_db_name}"
    
    # @property
    # def sql_server_uts_url_at(self) -> str:
    #     # "mssql+pymssql://username:password@localhost/sales_database"
    #     return f"mssql+pymssql://{self.uk_at_de_uts_user}:{self.uk_at_de_uts_password}@{self.uk_at_de_uts_host}/{self.at_uts_db_name}"
    
    # @property
    # def sql_server_uts_url_de(self) -> str:
    #     # "mssql+pymssql://username:password@localhost/sales_database"
    #     return f"mssql+pymssql://{self.uk_at_de_uts_user}:{self.uk_at_de_uts_password}@{self.uk_at_de_uts_host}/{self.de_uts_db_name}"
    
    # @property
    # def sql_server_uts_url_uk(self) -> str:
    #     # "mssql+pymssql://username:password@localhost/sales_database"
    #     return f"mssql+pymssql://{self.uk_at_de_uts_user}:{self.uk_at_de_uts_password}@{self.uk_at_de_uts_host}/{self.uk_uts_db_name}"
    



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
