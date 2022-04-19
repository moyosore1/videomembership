from email.policy import default
import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings, Field

# Pydantic is good for validation. Also, can be used to load env vars

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"


class Settings(BaseSettings):

    # dt of string "..." means field is required
    base_dir: Path = Path(__file__).resolve().parent
    templates_dir: Path = Path(__file__).resolve().parent / "templates"
    keyspace: str = Field(..., env='ASTRADB_KEYSPACE')
    db_client_id: str = Field(..., env='ASTRADB_CLIENT_ID')
    db_client_secret: str = Field(..., env='ASTRADB_CLIENT_SECRET')
    secret_key: str = Field(..., env='SECRET_KEY')
    jwt_algorithm: str = Field(default='HS256')
    session_duration : int = Field(default=86400)

    # .env file should be in directory uvicorn is called from

    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    return Settings()
