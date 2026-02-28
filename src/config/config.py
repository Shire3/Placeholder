import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    Project_Name: str = "Pizza Delivery API"
    Database_url: str = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES: int = os.getenv("JWT_ACCESS_TOKEN_EXPIRES")
    JWT_REFRESH_TOKEN_EXPIRES: int = os.getenv("JWT_REFRESH_TOKEN_EXPIRES")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", default="HS256")



settings = Settings()