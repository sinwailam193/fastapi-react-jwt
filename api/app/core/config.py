from os import path
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from jose.constants import ALGORITHMS

BASE_DIR = Path(__file__).resolve().parent.parent.parent


dotenv_file = BASE_DIR / ".env"
if path.isfile(dotenv_file):
    load_dotenv(dotenv_file)


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    DATABASE_URL: str
    DEVELOPMENT_MODE: bool = True
    SECRET_KEY: str
    ALGORITHM: str = ALGORITHMS.HS256

    # Auth setting
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
