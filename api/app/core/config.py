from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DEVELOPMENT_MODE: bool = True
    SECRET_KEY: str
    API_V1_STR: str = "/v1"

    # Auth setting
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
