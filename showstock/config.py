"""
Configuration module for the Showstock application.
Loads configuration from environment variables.
"""
import os
from typing import Optional
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database connection settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(env_prefix="SHOWSTOCK_DB_", env_file=".env", extra="ignore")
    
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    NAME: str = "showstock"
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800
    ECHO: bool = False
    
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        """Construct PostgreSQL connection URL from components."""
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            path=f"/{self.NAME}",
        )


class Settings(BaseSettings):
    """Main application settings."""
    
    model_config = SettingsConfigDict(env_prefix="SHOWSTOCK_", env_file=".env", extra="ignore")
    
    # Application settings
    APP_NAME: str = "Showstock"
    APP_DESCRIPTION: str = "Nutrition management for show livestock"
    DEBUG: bool = False
    
    # Database settings
    db: DatabaseSettings = DatabaseSettings()


# Create a global settings instance
settings = Settings()