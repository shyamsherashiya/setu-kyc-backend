from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    setu_client_id: str = Field(..., alias="SETU_CLIENT_ID")
    setu_client_secret: str = Field(..., alias="SETU_CLIENT_SECRET")
    setu_product_instance_id: str = Field(..., alias="SETU_PRODUCT_INSTANCE_ID")
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()