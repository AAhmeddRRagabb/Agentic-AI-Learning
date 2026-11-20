# ------------------------------------
# General CFG
# ------------------------------------

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

SENSITIVE_KEYWORDS = {
    "password",
    "password_hash",
    "credit_card",
    "credit card",
    "token",
    "secret",
    "api_key",
    "national_id",
}


DB_TABLES_EXIST = {
    "customers",
    "products",
    "orders",
    "sales",
    "categories",
    "countries"
}

DB_ALLOWED_QUERY_TYPES = {
    "select"
}


BASE_PATH = Path(__file__).resolve().parents[3]
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file          = BASE_PATH / '.env',
        env_file_encoding = "utf-8"
    )

    # API key
    GROQ_API_KEY  : str
    GOOGLE_API_KEY: str

def get_settings() -> Settings:
    return Settings()


